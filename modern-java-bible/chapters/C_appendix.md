# 부록 C. 마이그레이션 체크리스트

본문 20·20A·21장에서 우리는 마이그레이션의 *왜*와 *어떻게*를 길게 다뤘다. 이 부록은 실무에서 한 장 인쇄해서 *벽에 붙여놓고 줄을 그어가며* 쓸 수 있는 체크리스트다. 4단계로 나눴다 — 8 → 11, 11 → 17, 17 → 21, 21 → 25.

각 단계는 *건너뛰지 말자*. 8에서 21로 한 번에 이주하는 시도는 흔하지만, 단계마다 *고유한 함정*이 있어서 한꺼번에 처리하면 어디서 뭐가 깨졌는지 분간하기 어렵다. 단계별로 빌드를 통과시키고, CI를 녹색으로 만든 뒤 다음 단계로 넘어가는 편이 낫다.

---

## C.1 Step 1 — JDK 8 → JDK 11

가장 큰 충격원은 **Java EE 모듈 제거**(JEP 320)와 **Oracle JDK 라이선스 유료화**다. 빌드가 깨지는 자리 대부분이 이 둘이다.

### 빌드·런타임 환경

- [ ] JDK 배포본 결정 — OpenJDK·Temurin·Corretto·Liberica·Zulu 중 하나로 표준화
- [ ] 빌드 도구 최소 버전 확보 — Maven 3.6.3+, Gradle 7.3+
- [ ] CI/CD 파이프라인의 JDK 이미지 갱신
- [ ] 로컬 개발자 환경 — 모든 팀원 동일 JDK 버전·배포본 합의

### 코드 변경 — javax.* 제거 항목

- [ ] **JAXB**(`javax.xml.bind`) — `jakarta.xml.bind` + `org.glassfish.jaxb` 의존성 추가
- [ ] **JAX-WS**(`javax.xml.ws`) — `jakarta.xml.ws` + Metro·CXF로 이주
- [ ] **JTA**(`javax.transaction`) — `jakarta.transaction-api` 추가
- [ ] **CORBA**(`javax.activity`, `org.omg.*`) — 사용 중이면 별도 라이브러리 필요. 가능하면 *제거 권장*
- [ ] **javax.annotation**(`@PostConstruct`, `@PreDestroy` 등) — `jakarta.annotation-api` 추가
- [ ] **Nashorn**(`javax.script` ECMAScript 엔진) — 11에서 deprecation, 15에서 제거. GraalVM JS로 대체

### 내부 API·classpath

- [ ] `jdeps --jdk-internals` 실행 — `sun.*`·`com.sun.*` 사용처 식별
- [ ] `--add-opens`·`--add-exports`로 임시 허용 자리 목록화 (나중에 갚을 빚으로)
- [ ] reflection 기반 라이브러리(Lombok·Mockito·ByteBuddy) — 11 지원 버전 확인
- [ ] AspectJ 사용 시 — Java 11 호환 1.9.6+ 이상

### 빌드 인자

- [ ] `--release 11` 사용 — `-source`/`-target` 조합보다 안전
- [ ] Surefire/Failsafe — 2.22.2+ (모듈 시스템 인식)
- [ ] JaCoCo — 0.8.6+ (Java 11 bytecode 지원)

### 운영 환경

- [ ] **Docker 이미지 RSS 증가 대비** — JDK 8 대비 ~20% 증가 흔함. 컨테이너 memory limit 재산정
- [ ] G1이 default가 됨 — `-XX:+UseG1GC`는 명시 불필요
- [ ] `CompressedOops` 기본 동작 변경 확인
- [ ] JFR·JMC 사용 시작 검토 — 11부터 오픈소스

### 검증

- [ ] 전체 테스트 통과
- [ ] 부하 테스트 — throughput·p99 latency를 8 baseline과 비교
- [ ] 프로덕션 카나리아 배포 — 최소 1주

---

## C.2 Step 2 — JDK 11 → JDK 17

이 단계의 핵심은 **Spring Boot 2.7 → 3.x**다. 사실상 *javax → jakarta* 패키지 이주가 가장 큰 작업이다. Spring을 안 쓴다면 훨씬 가볍다.

### 빌드·런타임 환경

- [ ] JDK 17 LTS 확보 — Temurin·Corretto·Liberica 17
- [ ] Maven 3.6.3+ / Gradle 7.5+ (Gradle 8 권장)
- [ ] Kotlin 사용 시 — 1.7.0+ (JVM target 17 지원)

### Spring Boot 3.x 이주

- [ ] **javax → jakarta** 패키지 import 변경 (대규모 sed/IDE 작업)
- [ ] Spring Boot 3.x baseline — Java 17
- [ ] Spring Security 6 — 설정 API 대거 변경 (`WebSecurityConfigurerAdapter` deprecated)
- [ ] Spring Data 3.x — repository 메서드 시그니처 변경 일부
- [ ] Hibernate 6 — query·LazyInitializationException 동작 변경
- [ ] application.properties — `spring.config.*` 키 일부 변경
- [ ] Actuator — 일부 엔드포인트 응답 형식 변경

### 언어 신규 기능 *도입 후보* (점진 적용)

- [ ] **records** — DTO부터 시작. 14~16에서 도입된 product type
- [ ] **sealed classes** — 도메인 모델의 *합 타입* 자리
- [ ] **pattern matching for `instanceof`** — `if (x instanceof Foo f) ...` 패턴
- [ ] **switch expression** — `case L ->`·`yield`
- [ ] **text blocks** — JSON·SQL·HTML 리터럴 정리

### 보안

- [ ] **SecurityManager deprecation 영향 확인** — 17에서 deprecated. 25+ 완전 제거 예정
- [ ] `--add-opens` 필요 자리 재확인 — strong encapsulation default (JEP 403)
- [ ] **EdDSA** 사용 검토 (Ed25519·Ed448) — TLS·서명에서 RSA·ECDSA 대안

### 빌드 인자

- [ ] `--release 17`
- [ ] `--enable-preview` 사용처 식별 — preview 기능을 production에 쓰지 않기 권장
- [ ] JaCoCo 0.8.8+
- [ ] PIT mutation testing 1.9.0+ (사용 중이면)

### 운영 환경

- [ ] Generational ZGC (21에서 도입, 23 default) 대비 — 17에선 G1 또는 비-generational ZGC
- [ ] Container-aware CPU·memory 인식 자동화 (11+부터 default지만 재확인)
- [ ] JFR streaming 활용 검토

### 검증

- [ ] 컴파일·테스트 통과
- [ ] Spring Boot 3.x 통합 테스트
- [ ] 회귀 시나리오 — 인증·트랜잭션·캐시
- [ ] 프로덕션 카나리아 — 최소 2주 (Spring Boot 3.x 안정성 검증 필요)

---

## C.3 Step 3 — JDK 17 → JDK 21

이 단계의 *진짜* 변화는 **Virtual Threads**다. 도입 자체는 한 줄(`spring.threads.virtual.enabled=true`)이지만, *어디에 적용할지*가 가장 중요한 결정이다.

### 빌드·런타임 환경

- [ ] JDK 21 LTS 확보
- [ ] Spring Boot 3.2+ (virtual thread 통합 안정화 버전)
- [ ] Maven 3.9+ / Gradle 8.5+

### Virtual Thread 도입 후보 식별

- [ ] **I/O-bound 컨트롤러** — 외부 API·DB 호출이 주된 작업
- [ ] **batch / scheduled 작업** — 다수의 동시 작업이 I/O 대기 위주
- [ ] CPU-bound 작업은 *제외* — virtual thread의 이득 없음
- [ ] `spring.threads.virtual.enabled=true` 시범 적용 (스테이징 먼저)

### Pinning 위험 자리 audit (JEP 491 *이전*에는 특히 중요)

- [ ] **HikariCP 버전 확인** — 5.0.0+ (synchronized → ReentrantLock)
- [ ] **MySQL Connector/J** — 8.0.32+ (pinning 해소)
- [ ] **Postgres JDBC** — 42.5.0+ 권장
- [ ] **Caffeine 캐시** — 3.1.5+ (synchronized 제거)
- [ ] **Apache HttpClient** — 5.x 사용
- [ ] **MongoDB Java Driver** — 4.10+
- [ ] **Redis (Lettuce/Jedis)** — 최신 버전 확인
- [ ] **JFR `jdk.VirtualThreadPinned` 이벤트** 모니터링 활성화

### ThreadLocal 사용처 재검토

- [ ] **ThreadLocal 사용처 인벤토리** — 수백만 virtual thread 환경에서 메모리 폭발 위험
- [ ] **MDC**(SLF4J) — virtual thread에서 동작 검증
- [ ] **Security Context** — Spring Security의 `SecurityContextHolder`
- [ ] **트랜잭션 컨텍스트** — `TransactionSynchronizationManager`
- [ ] **ScopedValue 검토** (21 preview, 25 표준) — long-lived per-thread caching의 후임 후보

### 언어 신규 기능 *도입 후보* (점진 적용)

- [ ] **pattern matching for `switch`** — sealed exhaustive switch
- [ ] **record patterns** — `case Point(int x, int y) -> ...`
- [ ] **Sequenced Collections** — `getFirst`·`getLast`·`reversed` 활용
- [ ] **String Templates** — 21 preview였으나 23에서 철회. *도입 보류*

### 운영 환경

- [ ] **Generational ZGC 활성화 검토** — `-XX:+UseZGC -XX:+ZGenerational`
- [ ] 컨테이너 메모리 — ZGC는 off-heap 메타데이터 ~5% 추가 필요
- [ ] GC log 형식 — `-Xlog:gc*:file=...` (`-XX:+PrintGCDetails` deprecated)

### 검증

- [ ] virtual thread 시범 적용 — 컨트롤러 1~2개부터
- [ ] pinning 모니터링 — 1주간 JFR 이벤트 0건 확인
- [ ] 부하 테스트 — throughput·p99·메모리 사용량
- [ ] 프로덕션 카나리아 — 최소 2주

---

## C.4 Step 4 — JDK 21 → JDK 25

25는 *언어*보다 *런타임·메모리·시작 시간*의 LTS다. Virtual Thread를 이미 도입했다면 이 단계의 충격은 매우 작다. *측정 후 옵트인*이 키워드.

### 빌드·런타임 환경

- [ ] JDK 25 LTS 확보
- [ ] Spring Boot 3.4+ (CDS·AOT 통합)
- [ ] Maven 3.9.6+ / Gradle 8.10+

### Compact Object Headers (JEP 519)

- [ ] **벤치마크 — 옵트인 후 측정**: `-XX:+UseCompactObjectHeaders`
- [ ] heap 사용량 ~10~22% 감소 확인
- [ ] CPU·throughput·latency 회귀 확인 (드물지만 발생 가능)
- [ ] **production 적용 결정 — 측정값 기반**. default 아님

### AOT Class Loading & Linking (JEP 483 + 514·515)

- [ ] Spring Boot 3.4+ CDS 활성화 — `spring-boot-maven-plugin`의 `process-aot` goal
- [ ] training run → AOT cache 생성 흐름 CI에 편입
- [ ] startup time 측정 — Petclinic 기준 ~36~42% 단축
- [ ] cache 무효화 정책 — 배포 파이프라인에 통합
- [ ] *GraalVM Native Image와 비교* 결정 — AOT만으로 충분한지

### Virtual Thread `synchronized` (JEP 491)

- [ ] JDK 24+부터 `synchronized` pinning 해소
- [ ] 21~23에서 ReentrantLock으로 회피했던 자리 — *그대로 둘지* 결정
- [ ] 신규 코드는 `synchronized`도 안전 — 단, 라이브러리 호환성 확인

### Scoped Values (JEP 506 표준)

- [ ] ThreadLocal 사용처 — ScopedValue로 단계적 이주 검토
- [ ] 인증 컨텍스트·요청 ID·테넌트 ID 같은 *읽기 전용·범위 한정* 데이터 우선
- [ ] Spring Security 통합 — Spring 측 ScopedValue 지원 시점 확인 필요

### Structured Concurrency (JEP 505 preview)

- [ ] 25에서도 *preview* — production 사용은 신중
- [ ] StructuredTaskScope 시범 적용 — fan-out 자리 1~2건
- [ ] 표준화 일정 모니터링 — JDK 26 표준 후보

### 언어 신규 기능

- [ ] **Flexible Constructor Bodies** (JEP 513) — `super(...)` 전 statement 허용
- [ ] **Module Import Declarations** (JEP 511) — `import module java.base;` (학습·스크립트용)
- [ ] **Compact Source Files**·**Instance Main** (JEP 512) — `void main()` (학습용)
- [ ] **Stream Gatherers** (JEP 485, 24부터 표준) — 슬라이딩 윈도우·fold·scan 도입 검토

### 보안

- [ ] **SecurityManager 완전 제거 대비** (JEP 486, 25+에서 진행) — 사용처 모두 제거
- [ ] **KDF API** (JEP 510) — HKDF·PBKDF 표준 사용 가능
- [ ] post-quantum 준비 — KEM·KDF 표준 API 활용

### 운영 환경

- [ ] **Generational Shenandoah** (JEP 521) — Red Hat 환경 고려
- [ ] AOT 사용 시 — 컨테이너 이미지에 cache 포함
- [ ] CDS archive — image build 단계에서 생성

### 검증

- [ ] 컴파일·테스트 통과
- [ ] Compact Object Headers 측정 → 옵트인 결정
- [ ] AOT startup time 측정 → CI에 baseline 기록
- [ ] 프로덕션 카나리아 — 최소 1주 (25는 비교적 안전한 LTS)

---

## C.5 단계 전체에 걸친 *상시 항목*

단계와 무관하게 마이그레이션 작업 내내 챙겨야 할 항목들이다.

- [ ] **빌드 시간 변화 추적** — JDK 버전별 컴파일 시간을 CI에서 측정
- [ ] **의존성 호환성 매트릭스** 유지 — 팀 내부 위키에 라이브러리별 검증 버전 기록
- [ ] **롤백 계획** — 각 단계마다 이전 JDK로 되돌릴 수 있는 절차 문서화
- [ ] **카나리아 → 점진 배포** 흐름 — 모든 단계에서 동일
- [ ] **변경 사항 changelog** 작성 — 팀 외부(다른 팀·운영팀)에 영향 가는 변경 공유
- [ ] **JFR baseline** 캡처 — 단계 전·후 비교 가능하도록
- [ ] **deprecation 경고 0** 목표 — `-Xlint:deprecation` 활성화 후 점진 청소

---

## C.6 시간 견적 (참고치)

작은 서비스(코드 5만 LOC 이내, 의존성 30개 미만) 기준 *대략적인* 견적이다. 큰 모놀리스는 단계마다 ×3~5 곱해 보는 게 안전하다.

| 단계 | 코드 변경 | 검증 | 카나리아 | 합계 |
|---|---|---|---|---|
| 8 → 11 | 1~2주 | 1주 | 1주 | **3~4주** |
| 11 → 17 (Spring Boot 3 포함) | 2~4주 | 2주 | 2주 | **6~8주** |
| 17 → 21 | 1주 | 1주 | 2주 | **4주** |
| 21 → 25 | 0.5주 | 1주 | 1주 | **2~3주** |

11 → 17이 가장 무거운 이유는 *Spring Boot 3.x*와 *jakarta 패키지 이주* 때문이다. 21 → 25는 *언어 변화가 거의 없으니* 가벼운 편이다.

이 견적을 *팀 외부에 보고할 때*는 ×1.5 보정해 보고하자. 마이그레이션은 늘 예상보다 길게 끈다 — *난감한* 의존성 하나가 한 주를 통째로 잡아먹곤 한다. 시간 여유를 두고 잡는 편이 낫다.
