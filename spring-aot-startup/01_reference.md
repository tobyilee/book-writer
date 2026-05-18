# Spring 6/7 AOT 및 JVM 애플리케이션 시작 가속 기술 레퍼런스

> **대상 독자:** Spring 실무 경험이 있는 백엔드 중급+ 개발자
> **목적:** 350쪽 분량 단행본의 토대가 되는 종합 자료. 7개 핵심 기술과 그 주변 맥락을 깊이 있게 정리한다.
> **리서치 진행:** 2026-05-18. 공식 문서 + 컨퍼런스 세션 + 학술 논문 + 커뮤니티 후기를 교차 검증.

---

## 0. 큰 그림: "Java는 왜 느리게 시작하는가" — 문제 공간

Java 애플리케이션의 시작 지연은 단일 원인이 아니라 **다섯 가지 비용의 합**이다. 어떤 기술이 어느 비용을 줄이는지를 먼저 분류해야 책 전체의 비교 축이 명확해진다.

| 비용 단계 | 일어나는 일 | 해결하는 기술 |
|---|---|---|
| **A. JVM 부팅** | HotSpot 자체 초기화, 코어 클래스 로딩 | CDS, AppCDS |
| **B. 클래스 로딩·링킹** | 애플리케이션·라이브러리 클래스 파싱·검증 | AppCDS, Dynamic CDS, JEP 483 |
| **C. 프레임워크 초기화 (DI, 스캔)** | Spring의 ClassPath 스캔, @ComponentScan, @Conditional 평가, 리플렉션 | Spring AOT, Quarkus·Micronaut 빌드타임 DI |
| **D. JIT warm-up** | C1→C2 컴파일, 프로파일 수집, 최적화 | Project Leyden JEP 515, Azul ReadyNow, Alibaba JWarmup |
| **E. 첫 요청 처리** | 첫 트래픽이 들어와야 코드가 hot path로 진입 | Lazy init의 반대 효과, 의도적 워밍 |

같은 "시작 시간"이라는 단어 아래에 이 다섯 단계가 섞여 있다. 예를 들어 GraalVM Native Image는 A~D를 한꺼번에 제거하지만 E는 그대로 남는다(인터프리팅 단계가 없을 뿐). CRaC는 A~E를 통째로 우회한다. CDS는 A·B만 줄인다. 책의 모든 비교는 이 5단계 좌표 위에서 이뤄져야 한다.

---

## 1. 개념과 정의

### 1.1 Spring AOT Processing (Spring Framework 6 / Spring Boot 3)

Spring AOT는 **런타임에 일어나던 빈 정의 해석·조건 평가·프록시 결정을 빌드 타임으로 옮기는 처리기**다. 진입점은 `ApplicationContextAotGenerator`이며, `refreshForAotProcessing(hints)`을 호출해 빈 정의만 생성하고(인스턴스화는 하지 않음) `BeanFactoryInitializationAotProcessor` 구현체들을 순회한다 [출처: 웹, Spring Framework Reference Docs](https://docs.spring.io/spring-framework/reference/core/aot.html).

산출물은 세 종류다.

1. **생성된 Java 소스 코드** — 예를 들어 `DataSourceConfiguration__BeanDefinitions.java`가 만들어진다. 런타임에 리플렉션으로 `@Bean` 팩토리 메서드를 호출하던 코드가 직접 호출로 바뀐다.
2. **RuntimeHints** — 리플렉션·리소스·직렬화·JDK 프록시 사용 의도를 모은 JSON. GraalVM이 이걸 읽어 closed-world 분석에 반영한다.
3. **`ApplicationContextInitializer` 진입점** — 새 클래스가 컨텍스트 부팅의 시작점으로 등록된다.

활성화는 `-Dspring.aot.enabled=true` 또는 GraalVM Native Image 빌드 시 자동. **Spring Boot 3.x 일반 JVM 모드에서도 동작**한다는 점이 자주 간과된다 [출처: 웹, Javathinking blog](https://www.javathinking.com/blog/in-spring-boot-3-how-to-benefit-from-spring-aot-with-a-regular-jvm-application/).

핵심 API:
- `BeanFactoryInitializationAotProcessor` / `BeanFactoryInitializationAotContribution` — 빈팩토리 수준 기여
- `BeanRegistrationAotProcessor` / `BeanRegistrationAotContribution` — 개별 빈 수준 기여 (`@Autowired` 주입 코드 생성 등)
- `RuntimeHintsRegistrar` + `@ImportRuntimeHints` — 외부 라이브러리에 힌트 부여
- `@Reflective`, `@RegisterReflection` — 어노테이션 기반 힌트
- `META-INF/spring/aot.factories` — 프로세서 등록

### 1.2 GraalVM Native Image

OpenJDK가 아닌 **Substrate VM 기반의 별도 런타임**으로, 자바 바이트코드를 ELF/Mach-O/PE 네이티브 실행 파일로 AOT 컴파일한다. 핵심은 *closed-world assumption* — "런타임에 로드될 수 있는 모든 코드는 빌드 시점에 알려져야 한다" [출처: 웹, GraalVM Docs](https://www.graalvm.org/latest/reference-manual/native-image/metadata/).

빌드 파이프라인:
1. **points-to analysis** — 도달 가능한 코드를 정적 분석으로 결정 (Würthinger et al., OOPSLA 2019의 핵심 기여)
2. **heap snapshotting** — 빌드 타임에 실행된 static initializer의 결과 객체를 힙 이미지로 직렬화
3. **ahead-of-time compilation** — 도달 가능한 메서드를 Graal 컴파일러로 네이티브 코드 변환

런타임 시작은 **사전 채워진 힙(pre-populated heap)을 copy-on-write 매핑**으로 시작한다 [출처: 논문, "Initialize Once, Start Fast: Application Initialization at Build Time", Wimmer et al., OOPSLA 2019, DOI 10.1145/3360610](https://dl.acm.org/doi/abs/10.1145/3360610). 시작 성능이 HotSpot 대비 최대 **2 자릿수 배수**(up to two orders of magnitude) 향상된다고 보고됨.

도달성 메타데이터(reachability metadata):
- `reachability-metadata.json` — reflection / jni / resources / serialization / proxies 5개 섹션
- Spring 자체는 1st-party 힌트만 제공, 3rd-party는 `oracle/graalvm-reachability-metadata` 리포지토리 의존 [출처: 웹, GraalVM Reachability Metadata project](https://medium.com/graalvm/enhancing-3rd-party-library-support-in-graalvm-native-image-with-shared-metadata-9eeae1651da4)

PGO(Profile-Guided Optimization): `--pgo-instrument`로 instrumented 바이너리 생성 → 대표 워크로드 실행 → `default.iprof` 생성 → `--pgo`로 최종 빌드. **Oracle GraalVM Enterprise 한정**(Community Edition 없음). 효과는 약 6% 런타임 속도, 15% 바이너리 크기 감소. ML 기반 프로파일 추론이 기본값이라 PGO 안 써도 일부 이득 [출처: 웹, GraalVM PGO docs](https://www.graalvm.org/latest/reference-manual/native-image/optimizations-and-performance/PGO/).

### 1.3 CDS (Class Data Sharing) 계보

| 단계 | JEP | JDK | 무엇이 추가됐나 |
|---|---|---|---|
| CDS (원래) | — | 1.5 | 부트스트랩 클래스로더의 클래스만 공유 |
| AppCDS | JEP 310 | 10 | 시스템·플랫폼·커스텀 클래스로더까지 확장. 대규모 엔터프라이즈에서 JVM당 수십~수백 MB 메모리 절감 [출처: 웹, OpenJDK JEP 310](https://openjdk.org/jeps/310) |
| Dynamic CDS Archive | JEP 350 | 13 | `-XX:ArchiveClassesAtExit=<file>`로 종료 시점에 자동 아카이브. trial run + classlist 생성 단계 제거 [출처: 웹, OpenJDK JEP 350](https://openjdk.org/jeps/350) |
| Spring 통합 | — | Boot 3.3+ | `-Dspring.context.exit=onRefresh`로 빈 초기화까지만 돌리고 종료, 그 시점에 아카이브 덤프 [출처: 웹, Spring Boot CDS docs](https://docs.spring.io/spring-framework/reference/integration/cds.html) |

전형적 워크플로우:
```bash
# 훈련 단계
java -XX:ArchiveClassesAtExit=app.jsa -Dspring.context.exit=onRefresh -jar app.jar
# 운영 단계
java -XX:SharedArchiveFile=app.jsa -jar app.jar
```

벤치마크: 일반적으로 **15~30% 시작 단축**, Spring Boot 3.3+ 케이스에서 4.9s → 2.4s (51% 감소) 보고 [출처: 웹, Bell-SW Spring Boot CDS 가이드 + Gholamzadreza Medium](https://medium.com/@gholamzadreza/go-faster-with-java-25-leveraging-project-leyden-aot-to-cut-startup-time-and-cloud-costs-c4905531d956).

### 1.4 CRaC (Coordinated Restore at Checkpoint)

OpenJDK 프로젝트. **CRIU(Checkpoint/Restore In Userspace)를 사용해 실행 중인 JVM 프로세스의 메모리·스레드·CPU 상태를 디스크 이미지로 직렬화**한 뒤, 다른 시점·다른 머신에서 복원 [출처: 웹, BellSoft CRaC 가이드](https://bell-sw.com/blog/what-is-crac-a-guide-to-cutting-java-startup-and-warmup-from-minutes-to-milliseconds/).

핵심 API (`org.crac` 패키지):
```java
public interface Resource {
    void beforeCheckpoint(Context<? extends Resource> context) throws Exception;
    void afterRestore(Context<? extends Resource> context) throws Exception;
}
Core.getGlobalContext().register(resource);
```

Spring 통합 (Boot 3.2부터 자동, 3.4에서 성숙):
- Spring `Lifecycle` 인터페이스의 `stop()` / `start()`가 자동으로 호출됨
- 빈이 직접 `Lifecycle`을 구현하면 별도 CRaC 코드 없이 리소스 핸들링 가능
- `spring-context-indexer`, JDBC 커넥션 풀, 임베디드 톰캣 등 주요 빈이 이미 대응

가장 강력한 제약: **체크포인트 시점에 열린 파일 핸들·소켓이 없어야 한다**. 따라서 DB 커넥션, 임베디드 서버 포트 등은 모두 닫혔다가 restore 후 재오픈되어야 한다.

성능: Spring PetClinic 기준 CRaC는 baseline(fat jar) 대비 **약 84% 시작 단축**, Spring AOT + AOT cache 대비 56.6% 추가 단축 [출처: 웹, blog.rasc.ch 벤치마크](https://blog.rasc.ch/2026/04/spring-boot-startup.html). 복원 시간 자체는 100~수백 ms 수준.

#### AWS Lambda SnapStart — CRaC의 클라우드 현실화

AWS는 Lambda 런타임에 **커스텀 CRaC 컨텍스트를 내장**해서 SnapStart를 구현했다. Firecracker microVM이 자체 스냅샷 기능을 제공하므로, Lambda는 Init Phase 이후 microVM 자체를 스냅샷한 뒤 cold start 때 그 스냅샷에서 복원한다 [출처: 웹, AWS Lambda Compute Blog](https://aws.amazon.com/blogs/compute/starting-up-faster-with-aws-lambda-snapstart/).

- 적용 비용: 코드 변경 거의 불필요
- 효과: Java 함수 cold start **최대 10배** 단축
- 함정: `java.util.Random`의 시드, 데이터베이스 커넥션, 캐싱된 timestamp 등 "한 번만 생성되는 값"이 모든 실행 환경에 공유됨 — 이를 위해 CRaC 콜백으로 재초기화 필요

### 1.5 JVM Warmup — JIT 컴파일 계층과 그 캐싱

HotSpot의 tiered compilation:
- Tier 0: 인터프리터
- Tier 1~3: C1 (client) — 빠른 컴파일, 가벼운 최적화, 프로파일 수집
- Tier 4: C2 (server) — 느린 컴파일, 적극적 최적화

문제는 **C2 컴파일이 실제 트래픽을 받아본 후에야 시작**된다는 점. 트래픽이 들어오자마자 latency가 튀는 "warm-up spike" 패턴이 발생한다. 이는 특히 카나리·롤링 배포 시 SLA를 깨는 원인이 된다 [출처: 웹, Azul "Java Warmup and the Scaling Loop Problem"](https://www.azul.com/blog/java-warmup-and-the-scaling-loop-problem/).

#### 솔루션 1: Azul Zing / Prime (상용)
- **Falcon JIT** — LLVM 기반의 더 공격적인 최적화 컴파일러
- **ReadyNow** — 이전 실행의 프로파일을 디스크에 직렬화, 다음 실행에서 main 호출 전 hot method를 미리 컴파일
- **Compile Stashing / Cloud Native Compiler** — 동일 메서드의 컴파일 결과를 100대 인스턴스가 공유

#### 솔루션 2: Alibaba Dragonwell JWarmup (오픈소스)
2016년 알리바바 사내에서 시작. 사전 실행(pre-run) 단계에서 hot method 프로파일을 파일로 기록 → 정상 실행 시 JIT 스레드가 그 메서드를 main 호출 전에 미리 컴파일. ElasticHeap 같은 부가 기능과 함께 패키징됨 [출처: 웹, Alibaba Cloud Blog "Alibaba Dragonwell: Towards a Java Runtime for Cloud Computing"](https://assets.ctfassets.net/oxjq45e8ilak/T2zSvRNiiV7dKSixYpXij/03109f27cc33d87d85dff044f6dada90/100770_1555814710_Sanhong_li_Glimpse_into_Alibaba_Dragonwell_Towards_a_Java_runtime_for_cloud_computing.pdf).

#### 솔루션 3: Eclipse OpenJ9 Shared Class Cache + AOT
OpenJ9은 `-Xshareclasses`로 클래스 데이터와 함께 **AOT 컴파일된 네이티브 메서드 코드까지 공유 메모리에 저장**한다. 첫 실행 후 다음 실행부터는 즉시 네이티브 코드로 실행. 시작 42% 단축, 풋프린트 66% 감소 보고 [출처: 웹, Eclipse OpenJ9 Docs](https://eclipse.dev/openj9/docs/shrc/).

#### 솔루션 4: Project Leyden — JEP 483 / 514 / 515

OpenJDK의 종합 답안. "condenser"라는 개념으로 **점진적으로 작업을 더 이른 단계(빌드 타임, 첫 실행, 인스톨)로 이동**시킨다.

| JEP | JDK | 무엇 |
|---|---|---|
| 483 | 24 | Ahead-of-Time Class Loading & Linking. CDS를 확장해 클래스를 *로드+링크된 상태*로 캐싱. 워크플로우: 훈련 → 어셈블 → 운영 (3-step) |
| 514 | 25 | Command-Line Ergonomics. `-XX:AOTCacheOutput=app.aot` 한 줄로 훈련+어셈블 통합 (2-step) [출처: 웹, OpenJDK + Inside.java](https://inside.java/2026/01/09/run-aot-cache/) |
| 515 | 25 | Ahead-of-Time Method Profiling. 훈련 실행에서 hot method 프로파일을 캐시에 저장 → JIT가 부팅 즉시 사용 → C2 컴파일이 빨라짐 [출처: 웹, OpenJDK JEP 515](https://openjdk.org/jeps/515) |

벤치마크: Spring PetClinic 시작 **41% 단축**(Java 24, JEP 483), Helidon SE 67% / MP 62% [출처: 웹, InfoQ "Java Applications Can Start 40% Faster in Java 24"](https://www.infoq.com/news/2025/03/java-24-leyden-ships/). JEP 515 추가 시 warm-up 15~25% 추가 단축. AOT cache는 250KB 정도로 가볍다.

차세대 ("premain" 브랜치, 아직 메인라인 미통합):
- **JEP draft 8335368: AOT Code Compilation** — 훈련에서 사용된 메서드를 *컴파일된 네이티브 코드*까지 캐시에 저장. 결국 GraalVM Native Image와 유사한 결과를 OpenJDK에서 제공하게 될 것 [출처: 웹, openjdk/leyden premain README](https://github.com/openjdk/leyden/blob/premain/README.md).

### 1.6 Lazy Initialization

Spring Boot 2.2에 도입된 `spring.main.lazy-initialization=true`. **모든 `@Bean`이 첫 사용 시점에 생성**된다. 시작 시간 일부 감소(소규모 앱에서 2500→2000ms, 약 20%)이지만 트레이드오프가 크다 [출처: 웹, Spring Blog 2019 + Baeldung](https://spring.io/blog/2019/03/14/lazy-initialization-in-spring-boot-2-2/).

트레이드오프:
- **첫 요청 latency 증가** — 빈 초기화가 그 요청에 포함됨. 로드밸런서·오토스케일러가 첫 인스턴스를 정상으로 판단하기 어려움
- **에러 발견 시점 지연** — 빈 설정 오류, DB 미연결, 누락된 프로퍼티가 첫 사용 때까지 침묵
- **부분 적용 가능** — 전역 대신 `@Lazy`를 특정 빈에만 부여

권장 사용처: 개발 시 거의 항상 켜기. 운영은 워크로드에 따라.

### 1.7 부가 맥락 기술

#### Quarkus / Micronaut의 build-time DI

Quarkus(2018, Red Hat)와 Micronaut(2018, Object Computing)이 Spring보다 먼저 AOT로 갔다. **둘 다 컴파일 시점에 어노테이션 프로세서로 DI 코드를 생성**해 런타임 리플렉션을 거의 없앤다 [출처: 웹, 다수 비교 글](https://www.javacodegeeks.com/2025/12/spring-boot-vs-quarkus-vs-micronaut-the-ultimate-2026-showdown.html).

- **Micronaut**: Java APT(annotation processor)로 DI 클래스를 직접 생성. 리플렉션 없음.
- **Quarkus**: "augmentation phase"라는 빌드 페이즈에서 거의 모든 와이어링·설정을 사전 계산. 런타임은 사전 계산된 결과를 로드만 함.

Spring AOT는 결과적으로 같은 방향이지만 **기존 어노테이션·BeanDefinition 모델을 유지하면서** 빌드 타임 처리를 추가했다는 점이 다르다. 호환성 우선 설계의 결과.

#### 진단·프로파일링 도구

| 도구 | 용도 |
|---|---|
| Spring `BufferingApplicationStartup` + `/actuator/startup` | 빈별 초기화 시간 트리 [출처: 웹, amitph.com](https://www.amitph.com/spring-boot-startup-monitoring/) |
| `FlightRecordingApplicationStartup` | JFR로 시작 이벤트 기록 |
| `-XX:+PrintCompilation` | JIT 컴파일 로그 |
| async-profiler (JFR 호환) | flame graph, 시작 중 CPU 핫스팟 식별 |
| `-Xlog:class+load=info` | 클래스 로딩 시간 추적 |

#### 컨테이너·서버리스 cold start

서버리스 cold start 분해 [출처: 논문, "Cold Start Latency in Serverless Computing: A Systematic Review", Manner et al., arXiv 2310.08437, ACM Computing Surveys 2024, DOI 10.1145/3700875](https://dl.acm.org/doi/10.1145/3700875):
1. 스케줄링 지연 (Kubernetes/Knative 측)
2. 컨테이너·VM 부팅
3. 런타임 부팅 (JVM)
4. 함수 초기화
5. 첫 호출 처리

연구에 따르면 스크립트 언어(Python, JS) 대비 컴파일 런타임(Java, .NET)이 **최대 100배 cold start가 느릴 수 있다**. 그러나 JVM 측 가속 기술(SnapStart, Native Image)이 이 격차를 거의 0으로 압축한다.

Kubernetes 측 완화 기법:
- **HPA `cpu-initialization-period`** (기본 5분) — 부팅 중 CPU 스파이크를 스케일링 결정에서 제외
- **KEDA scale-to-zero** — HPA가 못 하는 0→1 스케일링을 외부 이벤트 기반으로 수행
- **N+2 버퍼 패드 패턴** — 평균 부하보다 2 파드 많이 유지

---

## 2. 핵심 관점 — 각 기술의 트레이드오프

### 2.1 "어디서 비용을 치를 것인가" 매트릭스

| 기술 | 빌드 시간 | 런타임 메모리 | 시작 시간 | 피크 성능 | 디버깅 난이도 | 동적 기능 |
|---|---|---|---|---|---|---|
| 일반 JVM | 짧음 | 보통 | 느림 | 최고 | 쉬움 | 완전 자유 |
| CDS / AppCDS | 짧음 | 약간 감소 | -15~30% | 동일 | 쉬움 | 자유 |
| Spring AOT (JVM 모드) | 약간 증가 | 약간 감소 | -10~20% | 거의 동일 | 약간 어려움 (생성 코드 디버깅) | 동적 빈 등록 제약 |
| JEP 483 AOT cache | 짧음 (훈련 1회) | 동일 | -40~50% | 동일 | 쉬움 | 자유 |
| JEP 483 + Spring AOT | 약간 증가 | 약간 감소 | -50~70% | 동일 | 보통 | 동적 빈 등록 제약 |
| CRaC / SnapStart | 짧음 (체크포인트 1회) | 동일 | -80~95% | 동일 | 어려움 (상태 외부화) | Linux 한정, 리소스 핸들링 강제 |
| GraalVM Native Image | **매우 김** (수 분~10분+) | **-50~75%** | **-95~99%** | 약간 낮음 (PGO 안 쓰면) | **매우 어려움** | 리플렉션·동적 클래스 로딩 사실상 차단 |

### 2.2 관점 A vs 관점 B — 자주 충돌하는 의견

**Q: GraalVM Native가 "최종 정답"인가?**

- **관점 A (Native 옹호):** 시작 50ms 미만, 메모리 절반 이하. 서버리스·짧은 수명 워크로드에 압도적. 컨테이너 이미지도 작아져 보안 표면이 줄어든다. Liberty Mutual은 5.7s → 655ms (9x 단축)을 프로덕션에서 달성 [출처: 웹, InfoWorld Liberty Mutual 사례](https://www.infoworld.com/article/4078803/taming-the-java-cold-start-beast-a-practical-guide-to-high-performance-serverless-with-graalvm-and-spring.html).
- **관점 B (Native 회의):** 빌드 시간이 1~10분으로 늘어 dev loop를 깬다. 리플렉션 사용 라이브러리마다 힌트가 필요해 호환성이 lottery. PGO는 Enterprise 한정. 피크 처리량은 JVM 대비 낮을 수 있다(특히 PGO 없을 때). 운영 중 진단(JFR, async-profiler 일부)이 제한적 [출처: 커뮤니티, velog 한국 후기 "GraalVM 도입 효과 비교 정리", "SpringBoot 3, GraalVM Native Image 적용 실패담", OKKY](https://velog.io/@profoundsea25/SpringBoot-3-GraalVM-Native-Image-%EC%A0%81%EC%9A%A9-%EC%8B%A4%ED%8C%A8%EB%8B%B4).

**책에서의 결론 권장:** 둘 다 살려두자. "워크로드 모양에 따라 다르다" — 짧은 cold start가 중요한 함수형 워크로드는 Native, 긴 수명의 백엔드 API는 CRaC 또는 JEP 483.

**Q: CRaC는 "치트키"인가, 운영 부담을 미루는 것인가?**

- **관점 A:** 시작 시간은 거의 0에 가깝게, 코드 변경은 거의 없게. 라이브러리 호환성도 GraalVM보다 훨씬 너그러움. Spring Boot 3.4부터는 자동.
- **관점 B:** 리눅스 전용. 보안 위험(메모리에 시크릿·세션 토큰이 그대로 직렬화될 수 있음 [출처: 웹, Spring Blog 2023 Sebastien Deleuze](https://spring.io/blog/2023/10/16/runtime-efficiency-with-spring/)). 체크포인트 시점에 열린 리소스가 모두 닫혀야 한다는 강한 제약. 운영 시 "체크포인트 → 배포 → restore"라는 추가 빌드 파이프라인 단계가 필요. 디버깅 가능한 노출 부담.

**Q: Project Leyden과 GraalVM 중 누가 이기는가?**

- **관점 A (Leyden 진영):** 점진적·후방호환. closed-world 제약 없음. 동일 코드 베이스가 동일 JVM에서 돌아간다. JEP 515가 warm-up까지 흡수하므로 결국 95%는 Leyden이 가져갈 것.
- **관점 B (GraalVM 진영):** Native Image는 단순한 startup 가속이 아니다 — **메모리 풋프린트와 보안 표면**까지 줄인다. Leyden AOT cache로는 메모리는 줄지 않는다. 컨테이너 이미지 100MB → 50MB의 차이는 Leyden이 절대 못 따라온다.
- **공식 입장 (Sébastien Deleuze, Spring Framework):** "둘 다 필요하다. Leyden은 'hardly any trade-off'의 길, Native는 trade-off가 있지만 그만한 값을 한다" [출처: 웹, Spring Blog "Runtime efficiency with Spring"](https://spring.io/blog/2023/10/16/runtime-efficiency-with-spring/).

### 2.3 빌드 vs 런타임의 철학 차이

Quarkus·Micronaut가 강조한 것은 "**리플렉션은 본질적으로 느린 게 아니라, 정보가 부족해서 느린 것**"이라는 통찰이다. 정보를 빌드 타임에 다 안다면 리플렉션은 정적 호출로 대체할 수 있다. Spring AOT는 같은 통찰을 후행적으로 받아들인 것 — 그래서 책 한 챕터는 "왜 Spring은 늦었나"를 다룰 만하다(이미 광범위한 reflection API를 노출했고 호환성을 깨면 안 되므로).

---

## 3. 대표 사례 (Production)

### 3.1 Netflix — Spring Boot 3 + Java 17 업그레이드

- **규모:** 3,000+ 애플리케이션, 1,500+ 라이브러리, 5명의 플랫폼 엔지니어
- **목표:** 보안 패치 받기, 시작 시간 단축, 미래 기반 마련
- **결과:** 평균 **15% 성능 향상** (시작 시간·처리량 종합)
- **포인트:** Native Image는 아직 채택 안 함. JVM 위에서 Spring Boot 3의 AOT 효과만으로 충분히 의미 있는 ROI [출처: 웹, VMware Tanzu Blog "How Netflix Increased Application Performance"](https://blogs.vmware.com/tanzu/how-netflix-increased-application-performance-with-spring-boot-3-and-java-17/)

### 3.2 Liberty Mutual — Spring Cloud Function + GraalVM on AWS Lambda

- **이전:** Spring Boot Lambda Init Duration **5,770 ms**
- **이후 (Native, Zip 배포):** **655 ms** — 9배 단축
- **이후 (Native, OCI 컨테이너):** 3.4s — ECR 다운로드 오버헤드로 오히려 회귀
- **워밍 후 빌드 duration:** 20 ms / 160 MB
- **함정:** Spring profiles 동적 해석 불가 → Lambda 환경변수로 외부화 [출처: 웹, InfoWorld 사례](https://www.infoworld.com/article/4078803/taming-the-java-cold-start-beast-a-practical-guide-to-high-performance-serverless-with-graalvm-and-spring.html)

### 3.3 Alibaba — Dragonwell + JWarmup at scale

- **컨텍스트:** 더블 일레븐(11.11) 트래픽 폭증에서 JIT warm-up이 1순위 병목
- **솔루션:** 사내 워크로드를 사전 실행해 hot method 프로파일을 분산 저장 → 신규 인스턴스 부팅 시 다운로드 + 사전 컴파일
- **2019년 Dragonwell GA 오픈소스화**. AJDK 8.1.1 (2016)부터 사내 사용. [출처: 웹, Alibaba Cloud Community](https://www.alibabacloud.com/blog/what-there-is-to-know-about-alibaba-dragonwell-8_595210)

### 3.4 AWS Lambda SnapStart — 산업 표준화

- **출시:** 2022년 re:Invent. Java Corretto 11/17, 이후 .NET, Python 확장
- **기술 스택:** Firecracker microVM 스냅샷 + 커스텀 CRaC 컨텍스트
- **효과:** Java cold start 최대 **10배** 단축, 추가 비용 없음
- **확장:** Spring Boot·Quarkus·Micronaut 모두 SnapStart에서 측정됨. Quarkus가 가장 빠르고 Spring Boot가 가장 호환성 좋음 [출처: 웹, "Cold starts with SnapStart for Java Frameworks", luafanti DEV](https://dev.to/luafanti/cold-starts-with-snapstart-for-java-frameworks-spring-boot-vs-quarkus-vs-micronaut-3hbf)

### 3.5 Azul — Cloud Native Compiler + ReadyNow Orchestrator

- **고객 패턴:** 트레이딩 시스템, 광고 입찰, 금융 — warm-up 시간에 돈을 잃는 워크로드
- **기술:** ReadyNow가 이전 실행 프로파일을 디스크에 저장, 같은 메서드를 100대 인스턴스가 각자 컴파일하던 것을 중앙 컴파일러가 1번만 컴파일해 공유
- **상용 한정** [출처: 웹, Azul docs](https://docs.azul.com/prime/analyzing-tuning-warmup)

### 3.6 Spring 공식 PetClinic 벤치마크 (2026-04)

| 전략 | 중앙값 시작 (ms) | baseline 대비 |
|---|---|---|
| baseline (fat jar) | 6,280.90 | — |
| Layer extraction | 5,295.53 | -15.7% |
| JEP 483 AOT cache | 2,698.56 | -57.1% |
| Spring AOT + AOT cache | 2,326.35 | -63.0% |
| CRaC | 1,010.33 | -83.9% |

[출처: 웹, blog.rasc.ch 종합 벤치마크](https://blog.rasc.ch/2026/04/spring-boot-startup.html)

### 3.7 Helidon — JEP 483 측정

- Helidon SE: -67%
- Helidon MP: -62%
- Quarkus도 자체 빌드 통합 발표 [출처: 웹, InfoQ Java 24 Leyden](https://www.infoq.com/news/2025/03/java-24-leyden-ships/)

---

## 4. 논쟁점·상충 관점

### 4.1 "Spring AOT vs Native vs CRaC — 무엇을 골라야 하나"

커뮤니티에서 가장 자주 묻는 질문. 정답이 아니라 **결정 트리**로 정리한다 [출처: 종합 — 웹·커뮤니티 다수].

```
워크로드가 "서버리스 함수 / 짧은 수명 / 메모리 비용 민감"인가?
├─ YES → Native Image (PGO 가능하면 PGO도) 또는 SnapStart (코드 변경 최소화 우선이면)
└─ NO → 긴 수명 백엔드 API?
        ├─ YES → CRaC (Linux 환경 + 운영 파이프라인 감당 가능시) 또는 JEP 483/515 (점진 도입 우선시)
        └─ NO (배치/CLI) → JEP 483 AOT cache가 가장 비용 대비 효과 큼
```

추가 변수:
- **개발팀 규모·역량** — Native Image 트러블슈팅은 사내 GraalVM 전문성 1명 이상 필수
- **라이브러리 다양성** — 비주류 라이브러리 많을수록 Native는 위험
- **컴플라이언스** — CRaC 스냅샷에 시크릿 노출 우려가 있는 산업(금융·헬스케어)은 Native 또는 CDS 선호

### 4.2 Reflection: 적인가 도구인가

- **GraalVM 관점:** 적이다. closed-world를 깬다. 정적 분석 불가능.
- **Spring 관점:** 도구다. 단, 가능하면 빌드 타임에 정보를 추출해 정적 호출로 대체.
- **현실 타협:** RuntimeHints API. "리플렉션은 쓰되, 어디서 어떻게 쓰는지 빌드 타임에 선언하라."

이는 단순한 기술 문제가 아니라 **에코시스템의 30년 자산을 어떻게 마이그레이션할 것인가**의 문제. 책에서 한 챕터 분량으로 풀 만하다.

### 4.3 Lazy init은 안티패턴인가

- **찬성:** 시작 시간이 신뢰성보다 중요한 dev 환경, 사용자가 거의 안 쓰는 빈이 많은 monolith에 유리.
- **반대:** 운영에서 fail-fast를 깨므로 위험. 첫 요청 latency 증가는 SLA 위반 가능.
- **타협:** 전역 대신 `@Lazy`를 거대 빈에만. 또는 lazy + readiness probe 분리.

### 4.4 Virtual Threads는 시작 가속과 어떤 관계인가

- **직접 관계 없음.** Loom은 *처리량* 문제, AOT는 *시작* 문제.
- **간접 관계:** Native + Loom 조합이 cold start 0 + 고동시성 처리량을 모두 달성할 수 있어 cloud-native 워크로드의 새 표준이 될 수 있다 [출처: 웹, Spring Blog "All together now"](https://spring.io/blog/2023/09/09/all-together-now-spring-boot-3-2-graalvm-native-images-java-21-and-virtual/).
- **함정:** `synchronized` 블록에서 virtual thread가 carrier에 pin됨. 시작 시간보다 운영 시 발견되는 함정.

### 4.5 PGO를 production에서 정말 돌릴 수 있는가

- **이론:** 대표 워크로드 → instrumented run → profile → 최종 빌드
- **현실:** instrumented 바이너리는 느려서 운영 불가. 대표 워크로드를 합성으로 만들기 어려움. ML 추론 프로파일(no PGO)이 기본값으로 자동 적용되므로 PGO 없이도 일정 이득이 있음 [출처: 웹, GraalVM PGO FAQ](https://www.graalvm.org/latest/reference-manual/native-image/optimizations-and-performance/PGO/faq/).
- **권장:** 워크로드가 안정적인 마이크로서비스에서만 PGO 도입. 빠르게 변하는 비즈니스 로직에서는 ML 프로파일에 의존.

---

## 5. 실무 적용 팁

### 5.1 단계별 도입 로드맵 (Spring 백엔드 팀 기준)

**Stage 0 (지금 당장, 코드 0줄):**
1. JDK 21+ 또는 가능하면 24+
2. Spring Boot 3.x로 업그레이드
3. CDS dynamic archive 적용 (`-XX:ArchiveClassesAtExit`)
4. `BufferingApplicationStartup`으로 빈별 시작 시간 측정

**Stage 1 (한 스프린트, 코드 약간):**
1. `-Dspring.aot.enabled=true` (JVM 모드 AOT) — 기존 코드 호환성 95%+
2. Spring AOT의 RuntimeHints 분석 후 잘못된 빈 등록 패턴 수정
3. CI 빌드 검증

**Stage 2 (분기 단위, 운영 변경):**
1. JEP 483 AOT cache (Java 24+)
2. Spring AOT + AOT cache 조합으로 50~60% 시작 단축
3. 훈련 워크로드를 CI에서 자동화

**Stage 3 (워크로드에 따라 선택):**
- 짧은 수명 → Native Image (GraalVM 전문성 확보 후)
- 긴 수명 → CRaC (Linux + 외부 시크릿 관리)
- AWS Lambda → SnapStart (가장 비용 대비 효과)

### 5.2 Spring AOT 적용 시 자주 깨지는 패턴

[출처: 웹, Spring Framework Reference + 커뮤니티 다수]

- `BeanDefinitionRegistry`로 런타임에 빈 등록 → 빌드 타임에 평가되도록 `ImportBeanDefinitionRegistrar`로 이동
- `@Bean` 메서드의 리턴 타입을 인터페이스로 선언 → 구체 타입으로 변경 (`MyImplementation` 반환)
- `@Profile`이 환경변수로 결정되도록 한 경우 → 빌드 타임에 고정되므로 별도 빌드 또는 환경변수로 다른 진입점
- 람다·메서드 레퍼런스로 빈 supplier 등록 → 명시적 클래스로 변경
- `LocalContainerEntityManagerFactoryBean` 스캔 → `PersistenceManagedTypesScanner`로 빌드 타임 스캔

### 5.3 GraalVM Native Image 트러블슈팅 체크리스트

1. **빌드 실패 시:** `--verbose --no-fallback`로 어떤 클래스가 missing인지 확인
2. **런타임 `NoSuchMethodException`:** 해당 메서드를 `reflect-config.json` 또는 `RuntimeHintsRegistrar`에 추가
3. **리소스 파일 못 찾음:** `hints.resources().registerPattern("dicts/*")` 같은 패턴 등록
4. **JDK 프록시 오류:** `hints.proxies().registerJdkProxy(MyInterface.class)`
5. **빌드 시간 10분+ :** PGO instrument 빌드는 더 오래 걸림. CI에 별도 잡 분리
6. **Tracing Agent 활용:** `-agentlib:native-image-agent=config-output-dir=./meta` 로 JVM 실행하면 자동으로 힌트 생성. 단 100% 커버리지는 아님

### 5.4 CRaC 적용 시 체크포인트

1. **체크포인트 전에 닫아야 할 리소스:**
   - JDBC 커넥션 풀 (HikariCP는 자동)
   - 임베디드 톰캣/네티 서버
   - 파일 핸들
   - 외부 API용 HTTP 클라이언트
2. **복원 후 다시 만들어야 할 것:**
   - `java.util.Random` 시드
   - 캐시된 timestamp / UUID
   - DB·Redis 커넥션
   - 메트릭/트레이싱 컬렉터
3. **보안:** 환경변수 시크릿이 체크포인트 이미지에 포함되지 않도록 KMS 등으로 외부화
4. **테스트 전략:** 체크포인트 → 다른 머신에서 restore → 통합 테스트 통과 확인을 CI에 포함

### 5.5 진단 워크플로우

[출처: 웹, async-profiler 가이드 + Spring docs 종합]

```bash
# 1. 빈별 시작 시간
curl localhost:8080/actuator/startup | jq

# 2. JIT 컴파일 로그
java -XX:+PrintCompilation -jar app.jar 2> compile.log

# 3. async-profiler로 시작 flame graph
java -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,file=startup.html -jar app.jar

# 4. 클래스 로딩 시간
java -Xlog:class+load=info:classes.log -jar app.jar

# 5. CDS 효과 측정
java -Xshare:on -XX:+PrintSharedArchiveAndExit -jar app.jar
```

---

## 6. 참고문헌

### 6.1 공식 문서 (1차 자료)

- Spring Framework Reference, "Ahead of Time Optimizations." https://docs.spring.io/spring-framework/reference/core/aot.html
- Spring Boot Reference, "Checkpoint and Restore With the JVM." https://docs.spring.io/spring-boot/reference/packaging/checkpoint-restore.html
- Spring Framework Reference, "CDS." https://docs.spring.io/spring-framework/reference/integration/cds.html
- Spring Boot Reference, "GraalVM Native Image Support." https://docs.spring.io/spring-boot/reference/packaging/native-image/introducing-graalvm-native-images.html
- GraalVM Docs, "Reachability Metadata." https://www.graalvm.org/latest/reference-manual/native-image/metadata/
- GraalVM Docs, "Profile-Guided Optimization." https://www.graalvm.org/latest/reference-manual/native-image/optimizations-and-performance/PGO/
- OpenJDK, "Project Leyden." https://openjdk.org/projects/leyden/
- OpenJDK JEP 310, "Application Class-Data Sharing." https://openjdk.org/jeps/310
- OpenJDK JEP 350, "Dynamic CDS Archives." https://openjdk.org/jeps/350
- OpenJDK JEP 483, "Ahead-of-Time Class Loading & Linking." (JDK 24)
- OpenJDK JEP 515, "Ahead-of-Time Method Profiling." https://openjdk.org/jeps/515
- AWS Lambda Docs, "Improving startup performance with Lambda SnapStart." https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html
- CRaC Docs (GitHub). https://github.com/CRaC/docs
- Eclipse OpenJ9 Docs, "Class data sharing." https://eclipse.dev/openj9/docs/shrc/
- Azul Prime Docs, "Analyzing and Tuning Warm-up." https://docs.azul.com/prime/analyzing-tuning-warmup

### 6.2 Spring 팀 블로그

- Deleuze, S. (2021). "New AOT Engine Brings Spring Native to the Next Level." Spring Blog, 2021-12-09. https://spring.io/blog/2021/12/09/new-aot-engine-brings-spring-native-to-the-next-level/
- Deleuze, S. (2023). "Runtime efficiency with Spring (today and tomorrow)." Spring Blog, 2023-10-16. https://spring.io/blog/2023/10/16/runtime-efficiency-with-spring/
- Spring Team. (2023). "All together now: Spring Boot 3.2, GraalVM native images, Java 21, and virtual threads." Spring Blog, 2023-09-09. https://spring.io/blog/2023/09/09/all-together-now-spring-boot-3-2-graalvm-native-images-java-21-and-virtual/

### 6.3 학술 논문

- Wimmer, C., Stancu, C., Hofer, P., Jovanovic, V., Wögerer, P., Kelly, P. B., Würthinger, T. (2019). "Initialize Once, Start Fast: Application Initialization at Build Time." *Proceedings of the ACM on Programming Languages*, Vol. 3, No. OOPSLA, Article 184. DOI: 10.1145/3360610. https://dl.acm.org/doi/abs/10.1145/3360610
- Manner, J., Endreß, M., Heckel, T., Wirtz, G. (2024). "Cold Start Latency in Serverless Computing: A Systematic Review, Taxonomy, and Future Directions." *ACM Computing Surveys*. DOI: 10.1145/3700875. arXiv:2310.08437. https://arxiv.org/abs/2310.08437
- Galletta, A. et al. (2024). "CRIU — Checkpoint Restore in Userspace for computational simulations and scientific applications." arXiv:2402.05244. https://arxiv.org/abs/2402.05244
- Lin, C., Khazaei, H. (2021). "Performance Evaluation of Snapshot Methods to Warm the Serverless Cold Start." arXiv:2105.13894. https://arxiv.org/abs/2105.13894
- Singhvi, A. et al. (2021). "Mitigating Cold Starts in Serverless Platforms: A Pool-Based Approach." arXiv:1903.12221. https://arxiv.org/pdf/1903.12221
- (Ed.) arXiv:2504.17460. "A Lightweight Method for Generating Multi-Tier JIT Compilation Virtual Machine in a Meta-Tracing Compiler Framework." https://arxiv.org/abs/2504.17460
- Li, S. et al. (Alibaba). "Alibaba Dragonwell: Towards a Java Runtime for Cloud Computing." Conference paper PDF. https://assets.ctfassets.net/oxjq45e8ilak/T2zSvRNiiV7dKSixYpXij/03109f27cc33d87d85dff044f6dada90/100770_1555814710_Sanhong_li_Glimpse_into_Alibaba_Dragonwell_Towards_a_Java_runtime_for_cloud_computing.pdf

### 6.4 산업·실무 자료

- InfoQ, "Java Applications Can Start 40% Faster in Java 24." 2025-03. https://www.infoq.com/news/2025/03/java-24-leyden-ships/
- InfoQ, "Spring Boot and Azul JDK Support Java Startup Time Reducer CRaC." 2023-06. https://www.infoq.com/news/2023/06/crac-cracks-mainstream-adoption/
- InfoQ, "Spring Boot 3.2 and Spring Framework 6.1 Add Java 21, Virtual Threads, and CRaC." 2024. https://www.infoq.com/articles/spring-boot-3-2-spring-6-1/
- InfoWorld, "Taming the Java cold-start beast: A practical guide to high-performance serverless with GraalVM and Spring." (Liberty Mutual 사례) https://www.infoworld.com/article/4078803/
- AWS Compute Blog, "Starting up faster with AWS Lambda SnapStart." https://aws.amazon.com/blogs/compute/starting-up-faster-with-aws-lambda-snapstart/
- AWS Compute Blog, "Reducing Java cold starts on AWS Lambda functions with SnapStart." https://aws.amazon.com/blogs/compute/reducing-java-cold-starts-on-aws-lambda-functions-with-snapstart/
- AWS Containers Blog, "Using CRaC to reduce Java startup times on Amazon EKS." https://aws.amazon.com/blogs/containers/using-crac-to-reduce-java-startup-times-on-amazon-eks/
- Inside.java, "Run Into the New Year with Java's Ahead-of-Time Cache Optimizations." 2026-01. https://inside.java/2026/01/09/run-aot-cache/
- Inside.java, "Supercharge your JVM Performance with Project Leyden and Spring Boot." 2025-11. https://inside.java/2025/11/02/devoxxbelgium-leyden-supercharge-jvm-performance/
- VMware Tanzu Blog, "How Netflix Increased Application Performance with Spring Boot 3 and Java 17." https://blogs.vmware.com/tanzu/how-netflix-increased-application-performance-with-spring-boot-3-and-java-17/
- BellSoft, "How to use CDS with Spring Boot applications." https://bell-sw.com/blog/how-to-use-cds-with-spring-boot-applications/
- BellSoft, "What is CRaC? A guide to cutting Java startup and warmup from minutes to milliseconds." https://bell-sw.com/blog/what-is-crac-a-guide-to-cutting-java-startup-and-warmup-from-minutes-to-milliseconds/
- Red Hat Developer, "Speed up Java application startup time with AppCDS." 2024-01. https://developers.redhat.com/articles/2024/01/23/speed-java-application-startup-time-appcds
- IBM Developer, "Reducing cold start times in Knative." https://developer.ibm.com/articles/reducing-cold-start-times-in-knative/

### 6.5 벤치마크·튜토리얼

- rasc.ch, "Faster Spring Boot Startup with CRaC, Leyden, and Spring AOT." 2026-04. https://blog.rasc.ch/2026/04/spring-boot-startup.html
- Gholamzadreza, "Go Faster with Java 25: Leveraging Project Leyden AOT to Cut Startup Time and Cloud Costs." Medium. https://medium.com/@gholamzadreza/go-faster-with-java-25-leveraging-project-leyden-aot-to-cut-startup-time-and-cloud-costs-c4905531d956
- Piotr Minkowski, "Speed up Java Startup with Spring Boot and Project Leyden." 2026-03. https://piotrminkowski.com/2026/03/19/speed-up-java-startup-with-spring-boot-and-project-leyden/
- Ionut Balosin, "Application / Dynamic Class Data Sharing In HotSpot JVM." https://ionutbalosin.com/2022/04/application-dynamic-class-data-sharing-in-hotspot-jvm/
- Gunnar Morling, "Let's Take a Look at JEP 483." https://www.morling.dev/blog/jep-483-aot-class-loading-linking/
- Gunnar Morling, "Building Class Data Sharing Archives with Apache Maven." https://www.morling.dev/blog/building-class-data-sharing-archives-with-apache-maven/
- Baeldung, "Ahead of Time Optimizations in Spring." https://www.baeldung.com/spring-6-ahead-of-time-optimizations
- Baeldung, "Native Images with Spring Boot and GraalVM." https://www.baeldung.com/spring-native-intro
- Baeldung, "Lazy Initialization in Spring Boot." https://www.baeldung.com/spring-boot-lazy-initialization
- Baeldung, "Ahead-of-Time Class Loading & Linking." https://www.baeldung.com/java-aot-class-loading-linking
- amitph.com, "Enable Spring Boot Application Startup Metrics to Diagnose Slow Startup." https://www.amitph.com/spring-boot-startup-monitoring/

### 6.6 커뮤니티·한국어 자료

- velog.io, "Spring GraalVM Native Image 띄어보기" (@akfls221). https://velog.io/@akfls221/Spring-GraalVM-Native-Image
- velog.io, "SpringBoot 3, GraalVM Native Image 적용 실패담" (@profoundsea25). https://velog.io/@profoundsea25/SpringBoot-3-GraalVM-Native-Image-%EC%A0%81%EC%9A%A9-%EC%8B%A4%ED%8C%A8%EB%8B%B4
- velog.io, "GraalVM 도입 효과 비교 정리" (@harperkwon). https://velog.io/@harperkwon/GraalVM-%EB%8F%84%EC%9E%85-%ED%9A%A8%EA%B3%BC-%EB%B9%84%EA%B5%90-%EC%A0%95%EB%A6%AC
- OKKY, "GraalVM은 아직 전격적으로 도입하기엔 무리인듯 하네요." https://okky.kr/articles/1432613
- Junhyunny Devlogs, "Spring Boot Supports GraalVM Native Image." https://junhyunny.github.io/java/spring-boot/spring-boot-supports-graal-vm-native-image/
- 엄범, "GraalVM으로 native image compile 하기 (with Spring Boot)." https://umbum.dev/2033/

### 6.7 Quarkus / Micronaut 비교

- Java Code Geeks, "Spring Boot vs Quarkus vs Micronaut: The Ultimate 2026 Showdown." 2025-12. https://www.javacodegeeks.com/2025/12/spring-boot-vs-quarkus-vs-micronaut-the-ultimate-2026-showdown.html
- SoftwareMill, "Comparing Java frameworks for cloud-native environments." https://softwaremill.com/comparing-java-frameworks-for-cloud-native-environments/
- Mill Build Tool blog, "Spring Boot, Micronaut and Quarkus with Mill." https://mill-build.org/blog/21-quarkus-spring-micronaut-with-mill.html
- DEV.to (luafanti), "Cold starts with SnapStart for Java Frameworks (Spring Boot vs Quarkus vs Micronaut)." https://dev.to/luafanti/cold-starts-with-snapstart-for-java-frameworks-spring-boot-vs-quarkus-vs-micronaut-3hbf

### 6.8 진단·도구

- Krzysztof Slusarski, "Async-profiler — manual by use cases." https://krzysztofslusarski.github.io/2022/12/12/async-manual.html
- BellSoft, "Profiling Java Docker containers with Async Profiler." https://bell-sw.com/blog/profiling-java-docker-containers-with-async-profiler/
- Baeldung, "A Guide to async-profiler." https://www.baeldung.com/java-async-profiler

---

## 7. 리서치 한계 (커버하지 못한 영역)

이 리서치가 350쪽 책의 토대로 충분하지만 다음 영역은 의도적으로 또는 자료 부족으로 얕게 다뤘다. 챕터 저술 단계에서 추가 조사가 필요하다.

### 7.1 한국 기업 프로덕션 사례 부재
토스·카카오·네이버·쿠팡 같은 한국 대형사가 CRaC·Native Image·Leyden을 프로덕션에 적용한 **회사 공식 기술 블로그 사례를 찾지 못했다**. 검색에서 잡힌 것은 개인 학습 블로그(velog)와 OKKY 토론 글뿐이다. 책에서 한국 독자에게 공감 가는 사례를 만들려면 다음 중 하나가 필요:
- 직접 인터뷰 / DM 수집
- 한국 컨퍼런스(Spring Camp, IF Kakao, DEVIEW) 발표 영상에서 사례 추출
- 영문 사례를 한국 백엔드 컨텍스트로 재해석(쿠팡 규모, 게임 서버 등 비유)

### 7.2 OpenJ9 깊이
Eclipse OpenJ9의 shared class cache + AOT가 사실 가장 오래된 운영 검증된 솔루션이지만, 채택률이 낮아 커뮤니티 자료가 IBM·Eclipse 공식에 편중되어 있다. 한 챕터 분량 이상 다루기엔 사용자 후기 데이터가 부족하다.

### 7.3 JEP 483의 한계와 실제 운영 함정
JDK 24/25가 너무 최근이라 1년 이상의 실전 운영 사례가 거의 없다. 커스텀 클래스로더 미지원, JVMTI agent 충돌, JFR과의 상호작용 같은 운영 함정이 본격적으로 드러나는 건 2026년 하반기일 것으로 예상.

### 7.4 GraalVM 내부 (points-to analysis, dataflow) 깊이
Würthinger et al. 2019 OOPSLA 논문 외에 Substrate VM 내부 구조를 깊이 다룬 학술 자료는 제한적. 책이 *사용자 관점* 책이라 큰 문제는 아니지만, "왜 closed-world가 필요한가"를 이론적으로 정당화하려면 추가 논문 발굴 필요(Sulong, Truffle 관련 OOPSLA·PLDI 논문 시리즈).

### 7.5 ZGC·Shenandoah와의 상호작용
시작 시간 단축 + 저지연 GC 결합 시나리오(예: CRaC + ZGC, Native Image + ZGC) 사례는 거의 없다. ZGC가 JEP 483과 JDK 26에서야 호환된다는 점만 확인됨. 

### 7.6 한국 비주류 라이브러리 호환성
한국에서 자주 쓰는 라이브러리(MyBatis 한글 매퍼, NHN Toast 라이브러리, 카카오·네이버 OAuth SDK 등)가 GraalVM에서 어떻게 동작하는지에 대한 데이터 없음. 책 후반부에 "당신의 스택은 준비되었나" 형태의 체크리스트로 다루되, 정확한 호환성은 독자 검증 영역으로 남길 것.

### 7.7 비용·ROI 분석
Lambda SnapStart는 "추가 비용 없음"으로 알려졌지만, **CRaC 환경 자체를 운영하는 데 드는 인프라 비용**(빌드 파이프라인, 체크포인트 저장소, 디버깅 도구) 데이터가 부족. 회사 규모별 ROI 계산은 책에서 가설로 다룰 수밖에 없다.

### 7.8 GraalVM의 라이선스·상용 정책 변화
PGO가 Enterprise 한정인 점, Oracle의 GraalVM 정책 변화(2024년 GFTC 라이선스)에 대한 비즈니스 컨텍스트가 얕다. 책에서 다룰 거면 변호사 검토 수준은 아니더라도 한 페이지 분량의 정리 필요.

---

**리서치 완료. 다음 단계:** Book Planning Lead가 이 자료를 기반으로 12+ 챕터 구조를 설계한다. 위 5단계 비용 모델(섹션 0)과 결정 트리(섹션 4.1)를 책 전체의 narrative spine으로 권장.
