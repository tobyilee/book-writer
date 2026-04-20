# JVM 내부 구조와 Garbage Collection 레퍼런스

## 1. 개념과 정의

### 1.1 JVM 아키텍처 개요

JVM(Java Virtual Machine)은 크게 세 가지 핵심 구성 요소로 이루어진다.

**클래스 로더 서브시스템(Class Loader Subsystem)**
- 런타임에 동적으로 클래스를 로딩·링킹·초기화하는 역할
- 세 가지 기본 클래스 로더: Bootstrap(핵심 Java 라이브러리), Extension(확장 라이브러리), Application(애플리케이션 클래스패스)
- 부모 위임 모델(Parent Delegation Model)을 통해 클래스 유일성과 보안을 보장
- 로딩(Loading) → 링킹(Linking: 검증·준비·해석) → 초기화(Initialization) 순서로 진행

**런타임 데이터 영역(Runtime Data Areas)**
- 프로그램 실행 중 JVM이 다양한 유형의 데이터를 저장하는 메모리 영역
- 힙, 스택, 메서드 영역, PC 레지스터, 네이티브 메서드 스택으로 구분

**실행 엔진(Execution Engine)**
- 바이트코드를 기계어로 변환하여 실행
- 인터프리터: 바이트코드를 한 줄씩 해석·실행
- JIT 컴파일러: 메서드 호출 횟수가 임계값에 도달하면 해당 메서드를 네이티브 코드로 컴파일하여 이후 호출 시 직접 사용 → 성능 향상
- 가비지 컬렉터: 사용하지 않는 메모리를 자동으로 회수

### 1.2 JVM 메모리 구조

**힙(Heap)**
- 모든 스레드가 공유하는 영역
- 객체 인스턴스와 배열이 할당되는 곳
- GC의 주된 대상 영역
- 고정 크기 또는 동적 확장/축소 가능, 연속 메모리일 필요 없음

**스택(Stack)**
- 스레드별 독립 존재 (thread-local)
- 메서드 호출 데이터 저장: 지역 변수, 메서드 인자, 반환 주소
- LIFO(Last-In-First-Out) 구조로 스택 프레임 관리
- 메서드 실행 완료 시 해당 스택 프레임 자동 제거

**메서드 영역(Method Area) / Metaspace**
- 모든 스레드가 공유
- 클래스 수준 메타데이터 저장: 클래스 구조, 메서드 데이터, 상수 풀, 정적 변수
- Java 7 이하: PermGen(Permanent Generation) → Java 8+: Metaspace(네이티브 메모리 사용)로 전환

**PC 레지스터(Program Counter Register)**
- 스레드별로 존재, 현재 실행 중인 바이트코드 명령의 주소를 저장

**네이티브 메서드 스택(Native Method Stack)**
- JNI를 통해 호출되는 네이티브 메서드의 실행 정보 저장

**변수 저장 위치 정리:**
| 변수 유형 | 저장 위치 |
|-----------|----------|
| 지역 변수 | 스택 |
| 인스턴스 변수 | 힙 |
| 정적 변수 | 메서드 영역 |

### 1.3 Garbage Collection 기본 원리

**Reference Counting (참조 카운팅)**
- 각 객체 헤더에 참조 카운터를 유지, 새 참조 생성 시 증가, 참조 제거 시 감소
- 카운터가 0이 되면 즉시 회수
- 단점: 순환 참조(Circular Reference) 해결 불가
- JVM에서는 사용하지 않음 (Python 등에서 사용)

**Mark-and-Sweep (마크 앤 스윕)**
- JVM이 실제 사용하는 추적(Tracing) 기반 알고리즘
- Mark 단계: GC Root(스택 프레임의 지역 변수, 정적 변수, JNI 참조 등)에서 시작하여 도달 가능한 모든 객체를 마킹
- Sweep 단계: 전체 메모리를 스캔하여 마킹되지 않은 객체의 메모리를 해제
- 단점: STW(Stop-The-World) 발생, 메모리 단편화(fragmentation) 가능

**Mark-Sweep-Compact**
- Mark-and-Sweep 후 살아남은 객체를 한쪽으로 압축(Compact)하여 단편화 해결
- 압축 과정에서 추가 STW 시간 발생

**Generational GC (세대별 가비지 컬렉션)**
- "대부분의 객체는 빨리 죽는다"는 약한 세대 가설(Weak Generational Hypothesis)에 기반
- Young Generation: 새로 생성된 객체가 위치, 빈번하고 빠른 Minor GC 수행
  - Eden 영역: 객체 최초 할당
  - Survivor 영역(S0, S1): Minor GC에서 살아남은 객체가 이동
- Old Generation: 여러 번 Minor GC를 생존한 객체가 승격(Promotion), Major/Full GC 대상
- 세대별 분리를 통해 GC 효율성을 극대화: Young 영역만 자주 수집하고 Old 영역은 드물게 수집

### 1.4 GC 알고리즘 종류

**Serial GC**
- 단일 스레드, STW 방식
- 힙 2GB 미만, CPU 2개 미만의 제한된 환경에 적합
- `-XX:+UseSerialGC`

**Parallel GC (Throughput Collector)**
- 멀티 스레드로 GC 병렬 수행, STW는 여전히 발생
- 배치 처리 등 처리량(throughput) 우선 워크로드에 적합
- CPU 코어 수에 비례하여 성능 확장
- `-XX:+UseParallelGC`

**CMS (Concurrent Mark Sweep) — Deprecated**
- 대부분의 마킹 작업을 애플리케이션 스레드와 동시 수행
- STW 시간을 최소화하려 했으나, 메모리 단편화 문제와 CPU 오버헤드
- Java 9에서 deprecated, Java 14에서 제거

**G1 GC (Garbage-First)**
- JDK 9부터 기본 GC (CPU 2개 이상, 힙 2GB 이상 환경)
- 힙을 고정 크기 리전(Region)으로 분할하여 증분 수집
- 가장 쓰레기가 많은 리전부터 우선 수집 → "Garbage-First"
- 동시(concurrent) 마킹 단계 포함하나, 대부분의 작업은 STW
- 지연 시간과 처리량의 균형점
- Java 25(JEP 523)에서 모든 환경의 기본 GC로 확대 (이전에 Serial로 폴백하던 환경 포함)
- `-XX:+UseG1GC`

**ZGC (Z Garbage Collector)**
- Oracle이 개발, JDK 11에서 실험적 도입, JDK 15에서 프로덕션 준비 완료
- 목표: 힙 크기와 무관하게 1ms 미만의 pause time
- **Colored Pointers**: 64비트 객체 참조의 상위 비트에 메타데이터(Marked0, Marked1, Remapped, Finalizable) 인코딩
- **Load Barriers**: 객체 참조 로드 시 배리어를 통해 재배치 중인 객체의 참조를 자동 수정 → 동시(concurrent) 재배치 가능
- JDK 21에서 Generational ZGC 도입, JDK 23에서 기본 모드로 전환
- 메모리 오버헤드: +20~30% (compressed oops 미지원, 동시 자료구조)
- `-XX:+UseZGC` (JDK 21+에서는 `-XX:+ZGenerational`이 기본)

**Shenandoah GC**
- Red Hat이 개발, OpenJDK에 포함
- 목표: 일관된 10ms 미만 pause time
- **Brooks Pointers (Forwarding Pointers)**: 각 객체에 현재 위치를 가리키는 추가 포인터 필드 유지 → 재배치 중에도 애플리케이션이 투명하게 객체 접근 가능
- ZGC와 달리 write-barrier 중심 접근 (ZGC는 read-barrier/load-barrier 중심)
- 메모리 오버헤드: +10~20% (Brooks 포인터로 인한 객체당 추가 워드)
- Oracle JDK에는 미포함, OpenJDK/AdoptOpenJDK/Red Hat 빌드에서 사용 가능
- `-XX:+UseShenandoahGC`

## 2. 주요 관점

### 2.1 GC 선택 기준: 워크로드별 가이드

| 워크로드 유형 | 권장 GC | 핵심 제약 |
|--------------|---------|----------|
| 마이크로서비스 (Spring Boot/Quarkus) | G1 GC | 2코어/2GB RAM 제약 |
| 레거시 JEE 시스템 | G1 GC | 힙 128GB까지 |
| 데이터 집약 (Spark/Flink) | Parallel GC | 순수 처리량 우선 |
| 초저지연 요구 | Generational ZGC | 25% 메모리 여유 필요 |
| 소형 컨테이너 | Serial GC | 100MB 미만 힙 |
| 비Oracle JDK + 저지연 | Shenandoah | Red Hat/OpenJDK 빌드 |

**선택 의사결정 트리:**
1. 리소스 제약 (< 2코어/2GB)? → Serial GC
2. 배치 처리 우선? → Parallel GC
3. 일반적 균형 잡힌 워크로드? → G1 GC
4. JDK 21+ 대규모 힙에서 1ms 미만 응답? → Generational ZGC
5. 비Oracle JDK에서 저지연 필요? → Shenandoah GC

### 2.2 GC 성능 삼각형: 지연(Latency) vs 처리량(Throughput) vs 메모리(Footprint)

세 가지 목표를 동시에 최적화하는 것은 불가능하며, 둘을 선택하면 나머지 하나를 희생해야 한다.

- **Parallel GC**: 처리량 최대화, 지연 시간은 희생
- **G1 GC**: 지연과 처리량의 균형점, 메모리 효율적
- **ZGC / Shenandoah**: 초저지연, 처리량과 메모리를 일부 희생

### 2.3 GC 튜닝 철학

실무에서의 핵심 원칙:

1. **기본값으로 시작**: GC 튜닝은 측정 후에만 수행. 기본 설정으로 시작하고 필요할 때만 튜닝
2. **하나의 GC를 깊이 이해**: GC를 하나 선택하고 그것을 중심으로 튜닝 — 대부분의 서버 워크로드에서 G1이 기본 선택
3. **프로덕션 부하에서 측정**: GC 동작은 프로덕션 수준 트래픽에서 극적으로 달라짐 → 항상 실제 트래픽 패턴으로 부하 테스트
4. **목표 두 가지만 선택**: 지연, 처리량, 메모리 중 두 가지만 선택하고 나머지는 양보

### 2.4 최신 동향 (Java 21+ / 2025-2026)

**Generational ZGC의 부상**
- JDK 21에서 도입, JDK 23에서 기본 모드
- 비세대 ZGC 대비: 메모리 사용량 75% 감소, 처리량 4배 향상, pause time 1ms 미만 유지
- P99 pause time 10~20% 개선 (JDK 17/21 비세대 대비)
- Apache Cassandra 테스트: 275 동시 클라이언트에서도 일관된 pause time 유지 (비세대 ZGC는 성능 저하)

**Java 25 (JEP 523)**
- G1이 모든 환경에서 기본 GC로 확대 (이전에 Serial로 폴백하던 환경 포함)
- G1의 remembered set 처리 및 mixed GC pause 스파이크 개선
- 향후 대규모 힙에서는 ZGC가 기본이 될 가능성

**Virtual Threads (Project Loom)과 GC**
- 가상 스레드는 플랫폼 스레드 대비 스레드당 수백 바이트로 시작 (vs 1MB)
- GC 압력 대폭 감소: 5만 태스크 벤치마크에서 가상 스레드는 2회 GC pause, 플랫폼 스레드(10스레드풀)는 14회 pause + 325ms 총 pause 시간
- G1이 백그라운드 정리 작업을 시작할 필요조차 없음 (가상 스레드 사용 시)
- I/O 중심의 고동시성 워크로드에서 가장 효과적, CPU 바운드에서는 개선 제한적

**GraalVM 네이티브 이미지**
- Spring Boot 3.2에서 가상 스레드 + GraalVM 네이티브 이미지 조합 지원
- Serial GC와 G1 GC로 가상 스레드 지원
- Graal 컴파일러가 컴파일 스레드별 isolate 사용 → GC 부담 감소, 컴파일 처리량 및 메모리 풋프린트 개선
- 런타임 컴파일 활성화 시 가상 스레드 미지원 (GraalVM 언어)

## 3. 대표 사례

### 3.1 Netflix: Generational ZGC 마이그레이션

- Netflix의 핵심 스트리밍 비디오 서비스 절반 이상이 JDK 21 + Generational ZGC로 운영
- G1 대비 동일하거나 더 나은 CPU 활용률에서 평균 및 P99 지연 시간 모두 개선
- 성능 트레이드오프 없이 ZGC 도입 성공
- **jvmquake** 도구 개발: GC에 소비된 시간을 "부채(debt)"로 모델링 — GC에 200ms 소비 시 부채 카운터에 200ms 추가, 프로그램 실행 시간이 부채를 상환. 부채가 임계값 초과 시 JVM을 사전적으로 종료하여 GC 루프 방지

### 3.2 Uber: GC 튜닝으로 수백만 달러 절약

- GC 최적화를 통해 CPU 소비 7만 코어 절감 → 수백만 달러 비용 절약
- HDFS NameNode 튜닝: `-Xmx160g -Xmn16g -XX:ParGCCardsPerStrideChunk=32k`
  - RPC 큐 대기 시간: 500ms → 400ms (20% 개선)
  - 최대 GC 시간: 22초 → 1.5초
  - GC 횟수: 90회 → 70회
- Presto: String Deduplication 비활성화 → 에러율 2.5% → 0.73%, GC pause 비율 6.59% → 3%
- Azul C4 GC 실험: CMS 대비 P90 지연 24ms → 17ms (29% 개선), 650GB 힙에서 대부분 pause 3ms 미만
- **교훈**: 메트릭 수집기의 backoff가 1초가 아닌 1ms로 설정되어 400Mbps 가비지 생성율 → 2,258회 GC pause (평균 177ms). 코드 수준 문제가 GC 성능에 직접 영향
- **교훈**: 전체 힙을 늘릴 때 Young Generation을 비례적으로 늘리지 않으면 ParNew GC 시간 35% 증가

### 3.3 LinkedIn: OS 수준 GC 최적화

- 32GB 힙(6GB Young)에서 시작, 40GB로 확장
- CMS 튜닝: `CMSInitiatingOccupancyFraction=92`, `MaxTenuringThreshold=2`, `ParGCCardsPerStrideChunk=32768`
- `AlwaysPreTouch`: 런타임 페이지 제로화 비용 제거
- `vm.swappiness=0`: 불필요한 페이지 스왑 방지
- 결과: Young GC pause 80ms → 40~60ms, P99.9 지연 100ms → 60ms
- **핵심 발견**: 당시 G1은 CPU 사용량 증가로 처리량과 지연 시간 모두 악화 → ParNew/CMS가 더 나은 결과 (이는 G1 초기 버전의 한계로, 현재는 크게 개선됨)
- **핵심 발견**: 백그라운드 IO 트래픽(OS 페이지 캐시 writeback)이 JVM의 GC 로깅을 블로킹하여 대규모 STW pause 유발

### 3.4 OOM(OutOfMemoryError) 트러블슈팅 사례

**주요 OOM 유형과 원인:**

| OOM 유형 | 원인 | 해결 |
|----------|------|------|
| Java heap space | 힙 할당 초과, 메모리 릭 | `-Xmx` 증가, 릭 수정 |
| GC overhead limit exceeded | 힙 거의 가득 + GC가 충분히 회수 못함 | 힙 증가 또는 할당률 감소 |
| Metaspace | 클래스 과다 로딩 (동적 프록시, 빈번한 재배포) | `-XX:MaxMetaspaceSize` 조정 |
| unable to create new native thread | 컨테이너 메모리 한계 + 스레드 풀 미제한 | 스레드 풀 바운딩, `-Xss` 조정 |

**프로덕션 사례 (4서버 시스템):**
- 하루 3회 이상 OOM 발생
- 원인: IHOP(InitiatingHeapOccupancyPercent)가 70%로 설정되어 concurrent marking이 너무 늦게 시작
- 해결: IHOP를 working set 크기에 맞게 조정 (단, working set과 동일하게 설정하면 GC가 상시 실행되어 CPU 소진)

### 3.5 한국 개발 커뮤니티 사례 (velog)

- "대규모 애플리케이션에서 짧은 수명 객체(요청/응답 처리 중 생성되는 임시 객체)가 매우 많으며, 이를 효율적으로 처리하는 것이 핵심"
- GC 튜닝의 목표: STW 시간 최소화
- 튜닝 요소: GC 종류 선택, 힙 크기 조절, Young/Old 비율 조절
- 고려 지표: GC 총 소요 시간, 발생 주기, 응답 시간

## 4. 논쟁점과 상충 관점

### 4.1 ZGC vs Shenandoah: 어떤 저지연 GC를 선택할 것인가?

**관점 A — ZGC 우선론:**
- 극한 메모리 압력에서 25~40배 더 나은 pause time
- Oracle 공식 지원, JDK 표준 포함
- Generational 모드로 메모리 효율성 대폭 개선
- 수 GB~수 TB 힙 지원, 대규모 시스템에 적합
- Netflix 등 대형 기업의 프로덕션 검증

**관점 B — Shenandoah 우선론:**
- 중간 수준 메모리 사용 시나리오에서 더 높은 처리량
- 지연과 처리량의 균형이 ZGC보다 나은 경우 있음
- 메모리 오버헤드가 상대적으로 적음 (10~20% vs 20~30%)
- Red Hat 생태계(OpenShift 등)에서 더 나은 지원

**핵심 트레이드오프:**
- ZGC: 지연 시간이 왕일 때 + 대규모 힙 → 최적, 그러나 처리량 오버헤드(load barrier + 동시 백그라운드 스레드)
- Shenandoah: 경량·버스트 워크로드 또는 처리량 균형이 중요할 때 → 더 나은 선택일 수 있음

### 4.2 G1이면 충분한가, 저지연 GC로 갈아타야 하는가?

**관점 A — G1이면 충분하다:**
- 대부분의 일반적 서버 워크로드에서 기본 선택으로 적합
- Java 25에서 모든 환경의 기본 GC로 확대
- 지속적으로 개선 중 (remembered set, mixed GC 최적화)
- 메모리 효율성이 ZGC/Shenandoah보다 우수
- 튜닝이 비교적 단순

**관점 B — 저지연 GC로 전환해야 한다:**
- Netflix 사례: G1 대비 ZGC가 동일/더 나은 CPU에서 지연 시간 개선
- P99/P999 지연이 중요한 서비스에서는 G1의 STW가 문제
- Generational ZGC의 성숙으로 이전의 메모리/처리량 우려가 크게 완화
- 향후 ZGC가 대규모 힙의 기본이 될 가능성

### 4.3 GC 튜닝 vs 코드 최적화: 어디에 먼저 투자해야 하는가?

**관점 A — 코드 최적화 우선:**
- Uber 사례에서 메트릭 수집기의 1ms backoff 버그가 400Mbps 가비지 생성 → GC 튜닝으로는 해결 불가
- 객체 할당률(allocation rate) 자체를 줄이는 것이 GC 부담을 근본적으로 해소
- 불필요한 객체 생성, 박싱/언박싱, 임시 문자열 연결 등 코드 수준 개선이 선행되어야 함

**관점 B — GC 튜닝 우선:**
- 적절한 GC 선택과 힙 크기 설정만으로도 극적인 개선 가능 (Uber NameNode: GC 시간 22초 → 1.5초)
- 레거시 코드 수정이 어려운 경우 GC 튜닝이 현실적 대안
- JVM 옵션 변경은 코드 변경 대비 리스크와 비용이 낮음

**실무 합의:** 두 접근 모두 필요. 코드 수준의 과도한 할당을 먼저 확인 후, GC 튜닝으로 미세 조정하는 것이 가장 효과적.

### 4.4 Virtual Threads는 GC 문제를 해결하는가?

**관점 A — GC 부담을 획기적으로 줄인다:**
- 벤치마크: GC pause 2회 vs 14회(플랫폼 스레드), 총 pause 시간 대폭 감소
- 태스크가 빠르게 완료되어 단기 객체가 즉시 해제 → 힙 압력 최소화
- I/O 바운드 고동시성 서비스에서 극적 효과

**관점 B — 만능은 아니다:**
- CPU 바운드 워크로드에서는 개선 제한적 (스레드가 지속적으로 활성)
- 가상 스레드 자체도 메모리를 사용하며, 수백만 개 생성 시 누적 가능
- 학술 연구: 가상 스레드가 GC pause를 낮추지만, 메모리 트레이드오프가 존재 (특히 Shenandoah에서 관찰)

### 4.5 ML 기반 GC 자동 튜닝의 실현 가능성

- Inside.java(2025)에서 소개된 논문: ML 알고리즘이 GC 로그에서 추출한 정보를 기반으로 최적 JVM 플래그 값(특히 Young Generation 크기 관련)을 제안할 수 있는지 연구
- 아직 초기 연구 단계이나, 수동 튜닝의 복잡성을 고려할 때 자동화 방향은 유망
- ZGC의 자동 힙 사이징 JEP 초안이 진행 중 → "플래그 제로" GC 최적화를 향한 움직임

## 5. 실무 적용 팁

### 5.1 핵심 JVM 옵션

```bash
# 기본 힙 설정 (프로덕션에서 Xms = Xmx 권장)
-Xms4g -Xmx4g

# GC 선택
-XX:+UseG1GC          # 기본 (JDK 9+)
-XX:+UseZGC           # 저지연 (JDK 21+)
-XX:+UseShenandoahGC  # 저지연 (OpenJDK)

# GC 로깅 (JDK 9+)
-Xlog:gc*:file=gc.log:time,uptime,level,tags

# OOM 시 힙 덤프
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dumps/

# 컨테이너 환경
-XX:+UseContainerSupport  # Java 8u191+ / Java 10+
```

### 5.2 GC별 주요 튜닝 파라미터

**G1 GC:**
- `-XX:MaxGCPauseMillis=200` (목표 pause time)
- `-XX:InitiatingHeapOccupancyPercent=45` (concurrent marking 시작 임계치)

**ZGC:**
- `-XX:SoftMaxHeapSize` (소프트 힙 상한)

**Shenandoah:**
- `-XX:ShenandoahGCHeuristics=adaptive` (휴리스틱 모드)
- concurrent thread 수 조정

### 5.3 모니터링 도구

| 도구 | 용도 | 비용 |
|------|------|------|
| JVisualVM / JConsole | 실시간 힙, 스레드, GC 모니터링 | 무료 (JDK 포함) |
| JFR (Java Flight Recorder) | 저오버헤드 프로파일링, GC 이벤트 수집 | 무료 (JDK 11+) |
| GCViewer | GC 로그 분석 및 시각화 | 무료 |
| GCeasy | GC 로그 분석 (웹 기반) | Freemium |
| Datadog / New Relic | APM + GC 메트릭 통합 모니터링 | 유료 |

### 5.4 힙 사이징 가이드라인 (Uber 사례 기반)

- 전체 힙은 가용 RAM의 75% 이하로 설정
- Young Generation은 전체 힙의 20~50%
- 전체 힙은 측정된 최대 메모리 풋프린트보다 20% 크게 설정
- 전체 힙 증가 시 Young Generation도 비례적으로 증가시킬 것
- String Deduplication: 200GB+ 힙에서는 오버헤드 주의

### 5.5 컨테이너 환경 주의사항

- `-XX:+UseContainerSupport`로 컨테이너 메모리 한계 인식
- 힙 크기를 컨테이너 메모리 한계에 맞게 명시적 설정
- 네이티브 메모리(Metaspace, 스레드 스택, NIO 버퍼 등)를 위한 여유 확보 필요
- OOM Killer를 방지하기 위해 힙 + 비힙 메모리 합계가 컨테이너 한계 내에 있어야 함

## 6. 참고문헌

### 공식 문서 및 스펙
- [JVM Specification: The Structure of the Java Virtual Machine](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-2.html)
- [JEP 333: ZGC - A Scalable Low-Latency Garbage Collector](https://openjdk.org/jeps/333)
- [JEP 439: Generational ZGC](https://openjdk.org/jeps/439)
- [JEP 523: Make G1 the Default Garbage Collector in All Environments](https://openjdk.org/jeps/523)
- [Introducing Generational ZGC - Inside.java (2023)](https://inside.java/2023/11/28/gen-zgc-explainer/)
- [JDK 25 G1/Parallel/Serial GC changes](https://tschatzl.github.io/2025/08/12/jdk25-g1-serial-parallel-gc-changes.html)

### 기업 기술 블로그
- [Netflix: Bending Pause Times to Your Will with Generational ZGC](https://netflixtechblog.com/bending-pause-times-to-your-will-with-generational-zgc-256629c9386b)
- [Uber: Tricks of the Trade - Tuning JVM Memory for Large-scale Services](https://www.uber.com/us/en/blog/jvm-tuning-garbage-collection/)
- [LinkedIn: Garbage Collection Optimization for High-Throughput and Low-Latency Java Applications](https://engineering.linkedin.com/garbage-collection/garbage-collection-optimization-high-throughput-and-low-latency-java-applications)
- [LinkedIn: Eliminating Large JVM GC Pauses Caused by Background IO Traffic](https://engineering.linkedin.com/blog/2016/02/eliminating-large-jvm-gc-pauses-caused-by-background-io-traffic)
- [Netflix: Introducing jvmquake](https://netflixtechblog.medium.com/introducing-jvmquake-ec944c60ba70)

### 기술 블로그 및 튜토리얼
- [Baeldung: Generational ZGC in Java](https://www.baeldung.com/java-21-generational-z-garbage-collector)
- [Baeldung: Stack Memory and Heap Space in Java](https://www.baeldung.com/java-stack-heap)
- [Datadog: A Deep Dive into Java Garbage Collectors](https://www.datadoghq.com/blog/understanding-java-gc/)
- [foojay: The Ultimate 10-Years Java Garbage Collection Guide 2016-2026](https://foojay.io/today/the-ultimate-10-years-java-garbage-collection-guide-2016-2026-choosing-the-right-gc-for-every-workload/)
- [Sematext: JVM Performance Tuning Tutorial](https://sematext.com/blog/jvm-performance-tuning/)
- [GCeasy: Project Loom Memory Usage - Virtual Threads and GC](https://blog.gceasy.io/project-loom-memory-usage-java-virtual-threads-gc/)
- [GCeasy: ZGC vs Shenandoah Java GC](https://blog.gceasy.io/zgc-vs-shenandoah-java-gc/)
- [Gunnar Morling: Lower Java Tail Latencies With ZGC](https://www.morling.dev/blog/lower-java-tail-latencies-with-zgc/)
- [JVM Architecture and Workflow - DEV Community](https://dev.to/bugtobrilliance/jvm-architecture-and-workflow-understanding-the-java-virtual-machine-internals-17pg)
- [Java Code Geeks: G1 vs ZGC vs Shenandoah (2025)](https://www.javacodegeeks.com/2025/08/java-gc-performance-g1-vs-zgc-vs-shenandoah.html)
- [Java Code Geeks: ZGC vs Shenandoah Ultra-Low Latency (2025)](https://www.javacodegeeks.com/2025/04/zgc-vs-shenandoah-ultra-low-latency-gc-for-java.html)
- [Comparing Performance of Java 23 GC Algos - DEV Community](https://dev.to/vishalendu/comparing-java-23-gc-types-4aj)
- [IBM Community: G1, ZGC, and Shenandoah for Very Large Heaps (2025)](https://community.ibm.com/community/user/blogs/theo-ezell/2025/09/03/g1-shenandoah-and-zgc-garbage-collectors)
- [JVM Performance in 2025: Virtual Threads, GraalVM, and Containers](https://www.atruedev.com/blog/performance/jvm-performance-2025-virtual-threads-graalvm-containers)

### 학술 자료
- [ACM: Deep Dive into ZGC - A Modern Garbage Collector in OpenJDK](https://dl.acm.org/doi/full/10.1145/3538532)
- [A Performance Comparison of Modern Garbage Collectors for Big Data Environments (Goncalves 논문)](https://rodrigo-bruno.github.io/mentoring/77998-Carlos-Goncalves_dissertacao.pdf)
- [Evaluating Memory Management and GC Algorithms (Simatovic et al., 2025)](https://www.rit.edu/croatia/sites/rit.edu.croatia/files/docs/Evaluating%20memory%20management%20and%20garbage%20collection%20algorithms...,%20Simatovic%20et%20al.,%202025.pdf)
- [Optimizing GC for High-Performance Applications (IJSRET 2024)](https://ijsret.com/wp-content/uploads/2024/11/IJSRET_V5_issue5_478.pdf)
- [JVM Tuning with Machine Learning on GC Logs - Inside.java (2025)](https://inside.java/2025/01/13/thesis-jvm-tuning-ml/)
- [ZGC vs Shenandoah in Multithreaded Environments (Diva Portal 논문)](https://su.diva-portal.org/smash/get/diva2:1955686/FULLTEXT01.pdf)

### 한국어 자료
- [가비지 컬렉터(GC)에 대하여 - velog](https://velog.io/@litien/%EA%B0%80%EB%B9%84%EC%A7%80-%EC%BB%AC%EB%A0%89%ED%84%B0GC)
- [JVM 밑바닥까지 파헤치기 3장 - 가비지 컬렉터와 메모리 할당 전략 - velog](https://velog.io/@cksgodl/JVM-%EB%B0%91%EB%B0%94%EB%8B%A5%EA%B9%8C%EC%A7%80-%ED%8C%8C%ED%97%A4%EC%B9%98%EA%B8%B0-3%EC%9E%A5-%EA%B0%80%EB%B9%84%EC%A7%80-%EC%BB%AC%EB%A0%89%ED%84%B0%EC%99%80-%EB%A9%94%EB%AA%A8%EB%A6%AC-%ED%95%A0%EB%8B%B9-%EC%A0%84%EB%9E%B5)
- [JVM 가비지 컬렉션 메커니즘과 알고리즘 심층 분석 - velog](https://velog.io/@sjin/JVM-%EA%B0%80%EB%B9%84%EC%A7%80-%EC%BB%AC%EB%A0%89%EC%85%98GC-%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98%EA%B3%BC-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EC%8B%AC%EC%B8%B5-%EB%B6%84%EC%84%9D)
- [자바 메모리 관리 - 가비지 컬렉션 (yaboong)](https://yaboong.github.io/java/2018/06/09/java-garbage-collection/)
- [면접 질문: JVM, 가비지 컬렉션 - GitHub CS-study](https://github.com/hongcheol/CS-study/issues/138)

### OOM 트러블슈팅
- [HeapHero: Java OutOfMemoryError 9 Types, Causes & Solutions](https://blog.heaphero.io/types-of-outofmemoryerror/)
- [Sematext: Java OutOfMemoryError Exceptions Tutorial](https://sematext.com/blog/java-lang-outofmemoryerror/)
- [DZone: Root Causes of OOM Issues in Java Containers](https://dzone.com/articles/root-causes-of-OOM-issues-in-Java-containers)
- [Oracle: Understand the OutOfMemoryError Exception](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/memleaks002.html)
- [Java OOM Troubleshooting Guide - Production Best Practices (2025)](https://shayne007.github.io/2025/06/14/Java-OOM-Troubleshooting-Guide-Production-Best-Practices/)

## 7. 리서치 한계

### 커버하지 못한 영역

1. **Epsilon GC**: 메모리 회수를 수행하지 않는 no-op 컬렉터에 대한 심층 분석 미수행. 테스트/벤치마크 용도로만 사용되므로 대상 독자 관점에서 우선순위 낮음.

2. **OKKY 커뮤니티**: 한국 개발자 커뮤니티 OKKY의 구체적 토론 내용을 직접 수집하지 못함. velog 자료는 확보.

3. **Azul Zing/C4 GC 심층**: Uber 사례에서 언급되었으나, 상용 JVM인 Azul Zing의 C4 컬렉터에 대한 독립적 심층 분석은 미수행.

4. **JFR/VisualVM 실습 가이드**: 모니터링 도구에 대한 개념적 소개는 포함하나, 구체적 실습 단계별 가이드는 미포함. 챕터 저술 시 보강 권장.

5. **Kotlin/Scala 등 JVM 언어별 GC 특성 차이**: Java 외 JVM 언어에서의 GC 동작 차이(예: Kotlin 코루틴과 가상 스레드 비교)에 대한 조사 미수행.

6. **ARM 아키텍처에서의 GC 성능**: AWS Graviton 등 ARM 기반 서버에서의 GC 성능 차이에 대한 자료 미수집.

7. **GraalVM Native Image의 GC 제약사항 심층**: Serial GC 및 G1 지원은 확인했으나, 네이티브 이미지 환경의 GC 제약과 실무 임팩트에 대한 심층 분석은 제한적.
