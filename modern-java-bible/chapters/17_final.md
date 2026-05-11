# 17장. GC 11년의 진화 — Serial부터 Generational Shenandoah까지

Java 8의 `PermGen` OOM에 시달려본 사람이라면, 그 새벽의 알람 진동을 잊지 못할 것이다.

`java.lang.OutOfMemoryError: PermGen space`. 운영 중인 서비스가 갑자기 죽는다. heap은 멀쩡한데 PermGen이 꽉 찼다. `-XX:MaxPermSize=256m`을 올린다. 며칠 뒤 또 죽는다. ClassLoader 누수의 원인을 찾아 `Tomcat` 컨테이너의 webapp 재배포 로직을 헤매고, 결국 `-XX:MaxPermSize`를 512m으로 올리고 한숨을 쉰다. PermGen은 클래스 메타데이터를 담는 고정 영역이었고, 그 크기는 JVM 시작 시 못박혔다. 클래스가 늘어나면 죽었다. 무슨 일을 해도 *찜찜했다*.

Java 8이 PermGen을 없앤 건 그래서 사건이었다. 클래스 메타데이터를 native memory의 `Metaspace`로 옮겼다. heap이 아니다. JVM이 OS에서 직접 가져오는 메모리다. 기본값은 무제한 — `-XX:MaxMetaspaceSize`를 명시하지 않으면 시스템이 허락하는 만큼 늘어난다. PermGen OOM은 사라졌다. 그 자리에 다른 문제가 들어섰다. Docker 컨테이너의 `RSS`(Resident Set Size)가 슬금슬금 자라기 시작했다. CleverTap의 마이그레이션 회고가 짚어주듯, G1·JFR·Metaspace가 합산되면서 Docker OOM kill이 빈발했다([CleverTap Tech Blog](https://tech.clevertap.com/pitfalls-when-upgrading-from-java-8-to-java-17/)). heap 안의 OOM은 사라졌지만, 컨테이너 밖에서 *죽는* 새 패턴이 등장한 것이다.

11년이 지났다. 그사이 자바의 GC는 한 번 더, 그리고 또 한 번 더 옷을 갈아입었다. ZGC가 들어왔고, Shenandoah가 들어왔고, 둘 다 세대형으로 진화했다. Generational ZGC는 기본값이 됐고, 2025년 9월의 Java 25는 Shenandoah까지 세대형으로 만들어 냈다. 우리는 그동안 `-Xms`와 `-Xmx`만 만지면서 살아왔다. 그런데 — 솔직해지자. 우리 서비스는 어떤 GC를 써야 하는가? 그 질문에 한 문장으로 답할 수 있는 동료가 팀에 몇이나 있는가?

이 장은 그 질문에 답하기 위해 11년의 GC 지형을 한 장의 지도로 펼쳐 보이는 일이다. 9종의 GC가 차례로 들어왔다 사라졌고, 그 사이의 트레이드오프는 우리가 흔히 알고 있는 것보다 훨씬 정교하다. 함께 짚어보자.

## 9종의 GC 지형

먼저 한 번 정리하고 가자. 2026년 현재, OpenJDK가 손에 쥐고 있는 GC는 모두 아홉 종이다. 그중 하나(CMS)는 죽었고, 둘(Generational ZGC, Generational Shenandoah)은 새로 태어났다. 나머지는 그 사이에서 각자의 자리를 지키고 있다.

| GC | 첫 등장 | 메커니즘의 핵심 | 권장 사례 |
|---|---|---|---|
| Serial | 초기 | single-threaded, stop-the-world | embedded, 단일 CPU |
| Parallel | 1.4 | throughput 우선, 멀티스레드 STW | batch, throughput-bound |
| CMS | 1.4 (deprecated 9, removed 14) | concurrent old-gen mark-sweep | 옛 latency-sensitive — **사망** |
| **G1** | 7 (default 9+) | region-based, predictable pause | 일반 enterprise default |
| **ZGC** | 11 experimental, 15 production | colored pointers, sub-ms pause | 대용량 heap, low-latency |
| **Generational ZGC** | 21 (JEP 439), default 23 (JEP 474) | ZGC + 세대 분리 | 21+ default for low-latency |
| **Shenandoah** | 12 experimental, 15 production | concurrent compaction (Red Hat) | Red Hat ecosystem |
| **Generational Shenandoah** | 25 (JEP 521) | Shenandoah + 세대 | 25+ Red Hat 환경 |
| Epsilon | 11 (JEP 318) | no-op, 메모리 회수 안 함 | 테스트·short-lived |

표만 보면 단순하다. 그러나 이 한 줄짜리 칸들 안에는 11년의 설계 결정과 트레이드오프가 압축돼 있다. 하나씩 풀어보자.

**Serial과 Parallel은 여전히 살아 있다.** 우리가 자주 잊는 사실이다. Serial은 단일 CPU 환경, 작은 heap, 시작 시간이 짧아야 하는 짧은 lifecycle 프로세스에서 여전히 합리적이다. Parallel은 throughput을 최우선으로 둔 batch 작업에서 G1보다 나은 선택일 수 있다. STW pause가 길어도 상관없다면 — 그러니까 사용자 응답성을 신경 쓰지 않는 야간 ETL이라면 — Parallel의 throughput 우위가 빛난다. *잊지 말자*. 모든 워크로드가 sub-ms pause를 원하는 건 아니다.

**CMS는 죽었다.** JEP 363(Java 14)이 공식 사망 진단서다. concurrent mark-sweep으로 한때 latency-sensitive 자바의 사실상 표준이었지만, 단편화·복잡한 튜닝 노브·old-gen 단일화의 한계로 G1과 ZGC에 자리를 내줬다. 옛 코드베이스에서 `-XX:+UseConcMarkSweepGC` 플래그를 만나면 *반드시* 다른 GC로 갈아끼워야 한다. 14 이상에서는 그 플래그 자체가 인식되지 않거나 경고를 띄운다.

**G1은 사실상의 default다.** Java 9부터 server-class machine의 기본 GC가 됐고(JEP 248), 11년이 지난 지금도 압도적 다수의 Spring Boot 서비스가 G1 위에서 돌아간다. 핵심 아이디어는 *region-based*다. heap을 1~32MB 크기의 region으로 잘게 쪼개고, GC 사이클마다 *garbage가 가장 많은 region*을 우선 수집한다("Garbage First"). pause time을 직접 목표로 설정할 수 있다는 점이 매력이다 — `-XX:MaxGCPauseMillis=200`이라고 하면 G1은 그 목표를 향해 region 수집 개수와 cycle 빈도를 조절한다. *예측 가능한 pause*가 G1의 정체성이다.

**ZGC와 Shenandoah는 다른 방향에서 같은 문제를 풀었다.** "STW pause를 사실상 0에 가깝게 만들 수 없을까?" 둘 다 *concurrent compaction*을 답으로 내놨다. 객체 이동(compaction)을 애플리케이션 스레드와 동시에 수행한다. 그러나 *어떻게* 동시에 수행하느냐에서 갈렸다.

ZGC는 **colored pointers**(또는 load barriers)를 쓴다. 64비트 포인터에 GC 상태 비트를 박아 둔다. 객체에 접근할 때마다 그 비트를 읽고, 필요하면 forward — 즉, "이 객체는 이미 이사 갔다, 새 주소로 가라"라는 신호를 받아 새 주소로 redirect한다. 객체 이동 자체는 GC 스레드가 하고, 애플리케이션 스레드는 load 시점에 한 번 barrier 비용을 낼 뿐이다. pause는 mark 시작과 끝의 짧은 root scan뿐이고, 그것도 sub-millisecond 수준이다([ZGC: Production-Ready](https://openjdk.org/jeps/377)).

Shenandoah는 **Brooks pointer**(또는 forwarding pointer)를 쓴다. 모든 객체 헤더에 forwarding 슬롯을 하나씩 박아 놓는다. 객체 이동이 일어나면 그 슬롯에 새 주소를 적고, 접근하는 쪽이 forwarding을 따라간다. ZGC와 마찬가지로 sub-ms pause를 달성하지만, 메모리 오버헤드의 위치가 다르다 — ZGC는 포인터 자체에, Shenandoah는 객체 헤더에 비용을 둔다.

둘 다 결과는 비슷하다. heap이 1TB까지 늘어나도 pause는 millisecond 단위로 유지된다. G1이 약속한 "예측 가능한 pause"를 ZGC와 Shenandoah는 "거의 0인 pause"로 끌고 갔다.

**Epsilon은 농담이 아니다.** JEP 318(Java 11)으로 들어온 *no-op GC*다. 메모리를 회수하지 않는다. 할당만 하다가 heap이 차면 OOM으로 죽는다. 쓸모없는 것 같지만, GC 성능 측정의 baseline으로 매우 유용하다 — "GC가 없을 때의 처리량은 얼마인가?"를 측정하는 도구. 또 짧은 lifecycle batch 작업에서 *GC 자체의 비용*이 부담이라면, 충분한 heap을 주고 Epsilon으로 돌리는 선택도 있다. *기억해두자*. 자바는 GC가 없는 모드까지 갖고 있다.

여기까지가 지도다. 그러나 이 지도만으로는 "우리 서비스는 어떤 GC를 써야 하는가"에 답할 수 없다. 11년의 진화 *순서*를 따라 들어가 봐야 한다.

## ZGC의 11년 — experimental에서 default까지

ZGC의 여정은 자바 GC 진화의 척추다. 7년 만에 experimental에서 default로 올라온 이 GC의 궤적을 따라가면, 자바가 어떤 방향으로 가고 있는지가 보인다.

**JEP 248(Java 9)** — G1이 server-class 기본 GC가 됐다. 그전까지 Parallel이 default였다. 이 변경은 자바가 "throughput보다 predictable pause"로 무게중심을 옮긴 첫 신호다.

**JEP 333(Java 11)** — ZGC가 experimental로 들어왔다. "scalable, low-latency"라는 깃발을 들고. 당시 ZGC의 약속은 단순했다: heap 크기와 *무관하게* pause 10ms 이하. 그러나 experimental이었고, Linux/x64에서만 돌았고, JEP 333 원문이 명시하듯 "preliminary"라는 단어를 떼지 못한 상태였다.

**JEP 377(Java 15)** — ZGC가 production-ready 선언. 동시에 JEP 379로 Shenandoah도 production-ready. 두 GC가 같은 릴리스에서 정식 데뷔를 했다. 이때부터 *대용량 heap + low latency* 워크로드가 본격적으로 ZGC를 검토하기 시작했다.

**JEP 376(Java 16)** — Concurrent Thread-Stack Processing. ZGC가 thread stack을 stop-the-world 없이 처리할 수 있게 됐다. 이 변경으로 *사실상 모든* GC 작업이 concurrent가 됐다. STW pause는 sub-millisecond로 떨어졌다.

**JEP 439(Java 21)** — Generational ZGC. 가장 큰 진화다. 원래 ZGC는 단일 세대였다 — young/old 구분 없이 전체 heap을 한 번에 다뤘다. JEP 439는 ZGC에 *세대 분리*를 도입했다. 이유는 단순하다. "**대부분의 객체는 일찍 죽는다**"(generational hypothesis)는 30년 묵은 관찰을 ZGC도 활용하게 됐다. young region을 자주 청소하고 old region은 드물게 청소하면, 같은 throughput에 더 적은 메모리 오버헤드. JEP 439의 평가에 따르면 throughput이 ~10% 향상됐다.

**JEP 474(Java 23)** — Generational ZGC가 default. `-XX:+UseZGC`만 켜면 자동으로 generational이다. non-generational ZGC를 쓰려면 `-XX:-ZGenerational`을 명시해야 한다. JEP 474 원문은 default 변경의 의도를 "*대다수의 워크로드에서 더 낫기 때문*"이라고 표현한다([JEP 474](https://openjdk.org/jeps/474)). 11년 전 experimental로 들어온 GC가 default 자리로 올라온 것이다.

**JEP 521(Java 25)** — Generational Shenandoah. Red Hat 진영의 답이 한 박자 늦게 같은 방향으로 갔다. Shenandoah도 세대형이 됐다. ZGC가 23에 default를 차지한 상황에서 Shenandoah는 자기 진영의 사용자(Red Hat·OpenJDK distro)에게 같은 throughput 향상을 약속하면서 따라붙었다.

이 순서를 한 줄로 요약하면 이렇다. **GC는 "STW를 줄이는 경쟁"에서 "STW 없이 throughput까지 챙기는 경쟁"으로 옮겨 갔다.** sub-ms pause는 이제 기본 조건이고, 그 위에서 메모리 오버헤드를 어떻게 줄일지가 새 전장이다. 11년 전 PermGen OOM 알람에 새벽에 깨던 우리가 지금은 sub-ms pause를 "당연한 것"으로 다루는 시대에 와 있다.

## PermGen에서 Metaspace로 — 그리고 컨테이너의 함정

GC 9종의 지도를 살피기 전에, 우리가 한 번 멈춰 서서 정리해야 할 변화가 있다. 본문 첫 단락에서 잠깐 언급한 *PermGen 제거*다. 이 변경은 단순한 영역 이름 변경이 아니라, 자바 메모리 모델 전체와 컨테이너 환경의 상호작용을 바꿔놓은 사건이다.

Java 7까지의 PermGen은 클래스 메타데이터(클래스 구조, method bytecode, interned string)를 담는 *heap 안*의 고정 영역이었다. JVM 시작 시 `-XX:MaxPermSize`로 크기가 결정됐고, 그 한계를 넘으면 `OutOfMemoryError: PermGen space`로 죽었다.

Java 8(JEP 122)이 PermGen을 없애고 **Metaspace**를 도입했다. 클래스 메타데이터를 heap 밖, native memory로 옮겼다. `-XX:MaxMetaspaceSize`를 명시하지 않으면 기본값은 사실상 무제한이다. heap 안의 클래스 OOM은 사라졌다.

그런데 — 이 변화가 컨테이너 환경에서 *새로운 종류의 죽음*을 만들었다. *주의해야 한다*.

`docker stats`로 컨테이너의 메모리 사용량을 보면, 자바 프로세스의 RSS가 heap 크기보다 훨씬 크다. `-Xmx4g`로 설정한 컨테이너에서 RSS가 6GB를 찍는다. 어디로 갔는가? 답은 *off-heap 영역의 누적*이다.

- **Metaspace**: 클래스 메타데이터. 평범한 Spring Boot 앱이 200~400MB를 쓴다.
- **Direct memory**: `ByteBuffer.allocateDirect()`, Netty의 PooledByteBufAllocator.
- **JIT code cache**: `-XX:ReservedCodeCacheSize` 기본값이 240MB.
- **JFR buffer**: Java 11+의 Flight Recorder가 항상 켜져 있을 수 있다.
- **GC 메타데이터**: ZGC/Shenandoah의 remembered set, forwarding table.
- **Thread stack**: 스레드당 1MB, 200개면 200MB.

이 모두가 합쳐져 RSS가 된다. heap 4GB + 위의 합산 2GB → 6GB. 컨테이너 limit이 6GB라면, 트래픽 스파이크 한 번에 Docker OOM kill이 떨어진다. *컨테이너 밖에서* 죽는다. heap OOM 로그는 없다. JVM은 `SIGKILL`을 받고 그냥 사라진다.

CleverTap의 마이그레이션 회고가 이 패턴을 정확히 기록한다 — Java 8에서 17로 올린 뒤 G1 + JFR + Metaspace의 합산이 늘어나면서 Docker OOM kill이 빈발했고, 컨테이너 메모리 limit을 상향해야 했다([CleverTap Tech Blog](https://tech.clevertap.com/pitfalls-when-upgrading-from-java-8-to-java-17/)). PermGen은 사라졌지만, 그 자리에 *컨테이너의 OOM kill*이 들어선 것이다.

**해결의 원칙은 단순하다.** heap만 보지 말고, off-heap 합산을 보자. `-Xmx`만 정하지 말고 `-XX:MaxMetaspaceSize`, `-XX:MaxDirectMemorySize`, `-XX:ReservedCodeCacheSize`까지 명시하는 편이 낫다. 그리고 그 합산이 컨테이너 limit의 *80% 이하*에 들어오는지 확인하자. Java 10+부터는 `-XX:UseContainerSupport`가 기본으로 켜져 있어 cgroup limit을 인식하지만, 그것은 *heap 크기*를 컨테이너 limit에 맞춰 자동 조절할 뿐, off-heap까지 보호하지 않는다. *잊지 말자*.

> **벤치마크 박스 1: Netflix의 ZGC 도입** *(사실 확인 필요)*
>
> Netflix는 일부 streaming 워크로드에서 G1에서 ZGC로 전환한 사례를 공유했다. 핵심 지표는 *tail latency*다. G1 환경에서 p99의 GC pause가 200~400ms를 찍던 워크로드가, ZGC로 전환하면서 sub-10ms로 떨어졌다. 단 throughput은 약간 떨어졌고(ZGC의 barrier 비용), 메모리 footprint는 ~15% 증가했다. 적용 기준은 단순했다: "tail latency가 사용자 경험에 직접 영향을 주는 워크로드"에만 적용하고, throughput이 우선인 batch는 G1을 유지. *(구체 수치는 JFokus·Devoxx 발표 슬라이드 추가 확인 필요)*

> **벤치마크 박스 2: Pinterest·LinkedIn의 사례** *(사실 확인 필요)*
>
> Pinterest는 ad serving 인프라에서 ZGC 전환으로 p99 latency가 안정화됐다고 발표. LinkedIn은 large heap(>50GB) 워크로드에서 G1의 mixed collection cycle이 가끔 길어지는 문제를 ZGC로 해소. 두 사례 모두 *heap 크기 ≥ 16GB + latency-sensitive*가 적용 기준이었다. *(구체 수치 출처 확인 필요)*

> **벤치마크 박스 3: 일반 Spring Boot 서비스의 경험치**
>
> heap 2~4GB의 일반 REST API에서 G1 → ZGC로 갈아끼웠을 때 차이는 미미한 경우가 많다. ZGC의 강점이 "*대용량 heap에서 sub-ms pause*"인데, 작은 heap에서는 G1도 충분히 짧은 pause를 낸다. 오히려 ZGC의 native memory 오버헤드와 throughput 손실이 더 두드러진다. **8GB heap 미만이라면 G1을 유지하는 편이 낫다**는 권고가 IBM Community와 foojay의 GC 가이드에서 공통적으로 등장한다([IBM Community](https://community.ibm.com/community/user/blogs/theo-ezell/2025/09/03/g1-shenandoah-and-zgc-garbage-collectors), [foojay 10-year GC guide](https://foojay.io/today/the-ultimate-10-years-java-garbage-collection-guide-2016-2026-choosing-the-right-gc-for-every-workload/)).

## 어떤 GC를 골라야 하는가 — 세 워크로드 시나리오

자, 이제 가장 자주 묻는 질문에 답해보자. "우리 서비스는 어떤 GC를 써야 하는가?" 추상적으로 답하면 또 *찜찜한* 가이드가 된다. 세 가지 구체적인 워크로드를 놓고 따져보자.

**시나리오 A: Spring Boot REST API, heap 2GB, Kubernetes pod**

가장 흔한 케이스다. 결제 처리, 상품 조회, 사용자 인증 같은 OLTP 성격의 API 서버. 동시 요청 수백~수천, 응답시간 p99 200ms 이내. heap은 컨테이너 limit에 맞춰 2~4GB.

**선택: G1 (default 유지).** 별도 플래그를 줄 필요가 없다. Java 9 이상이라면 G1이 자동이다. 명시적으로 적자면 `-XX:+UseG1GC -XX:MaxGCPauseMillis=200` 정도. 이 워크로드에서 G1을 ZGC로 갈아끼우는 건 *대개 비용이 이득보다 크다*. heap이 작아서 ZGC의 강점이 드러나지 않고, off-heap 오버헤드는 컨테이너 limit 안에서 더 빠듯해진다.

추가로 챙길 것 — 컨테이너 limit을 정할 때 `-Xmx`의 1.5배 정도를 잡자. heap 2GB라면 컨테이너 3GB. 그 안에 Metaspace, direct memory, JIT cache, thread stack이 들어간다. `-XX:MaxRAMPercentage=60` 같은 옵션으로 heap을 cgroup limit의 비율로 자동 잡는 패턴도 안정적이다. *기억해두자*. 컨테이너의 OOM kill은 heap의 OOM과 다른 곳에서 온다.

**시나리오 B: 캐시 서버, heap 50GB**

Redis 대체로 in-memory cache를 자바로 구현한 서비스, 또는 Elasticsearch처럼 대용량 인덱스를 heap에 올려둔 서비스. heap이 50GB를 넘고, p99 latency 요구가 빡빡하다. 한 번의 GC pause가 100ms를 넘으면 사용자가 느낀다.

**선택: Generational ZGC.** `-XX:+UseZGC`(Java 23+에서는 자동으로 generational). 이 케이스가 ZGC가 만들어진 이유다. 50GB heap에서 G1의 mixed collection이 가끔 1초를 찍는 일이 있고, 그게 캐시 서버에서는 치명적이다. ZGC는 같은 heap에서 sub-10ms pause를 약속한다. throughput 손실은 있지만, latency 안정성이 우선이라면 받아들일 수 있다.

Red Hat 진영(RHEL의 OpenJDK)이라면 **Generational Shenandoah**(Java 25+)도 같은 자리에 들어온다. `-XX:+UseShenandoahGC`. 두 GC의 선택은 디스트리뷰션과 익숙함의 문제지, 성능 차이가 결정적이지 않다.

**시나리오 C: 야간 ETL 배치 잡**

매일 02:00에 도는 데이터 파이프라인. JDBC로 OLAP DB에서 수억 행을 읽어 가공해 다른 곳으로 적재. 응답시간은 무관 — 사용자가 보지 않는다. 단지 *전체 처리량*과 *총 실행 시간*이 중요하다.

**선택: Parallel GC.** `-XX:+UseParallelGC`. throughput을 최우선으로 두는 GC. pause가 100ms든 500ms든 상관없다. 같은 시간에 더 많은 행을 처리하는 게 이긴다. G1도 나쁘지 않지만, throughput으로만 비교하면 Parallel이 작은 차이로 앞선다.

극단으로 가면 **Epsilon**도 후보다. heap을 처리량의 *2배 이상*으로 넉넉히 잡고 `-XX:+UseEpsilonGC -XX:+UnlockExperimentalVMOptions`. GC가 아예 돌지 않으니 throughput이 최대다. 단 잡 끝나면 JVM이 OOM으로 죽거나 종료된다. 그 죽음을 *의도된 끝*으로 받아들일 수 있는 워크로드라면 — 짧은 lifecycle batch가 그렇다 — Epsilon은 거짓말 같은 throughput을 낸다.

이 세 시나리오만 익혀두자. 대부분의 결정이 이 셋의 변형이다. *권장형으로 말하자면* — 잘 모르겠으면 G1을 쓰는 편이 낫다. 그게 default인 데에는 이유가 있다. ZGC로 갈아끼우는 건 *latency 측정 데이터*가 손에 있을 때만 하자. 단순히 "최신 GC가 좋겠지"라는 직관으로 옮기면, throughput과 RSS 증가에 발목을 잡힌다.

## Spring Boot에서의 GC 튜닝과 진단

Spring Boot 컨테이너에서 GC를 다루는 일은 두 단계로 나뉜다. *측정*과 *튜닝*. 그런데 우리는 자주 측정 없이 튜닝부터 한다 — `-XX:+UseG1GC -XX:MaxGCPauseMillis=100`을 어디선가 베껴 와서 붙인다. 이건 *번거롭다*. 측정부터 짚어보자.

**JFR(Java Flight Recorder)로 GC pause 진단하기.** Java 11에서 오픈소스화된 JFR은 production-grade 프로파일러다. 항상 켜두는 비용이 낮다(~1% 미만 오버헤드). GC 이벤트를 빠짐없이 기록한다.

```bash
java -XX:StartFlightRecording=duration=60s,filename=app.jfr,settings=profile \
     -jar app.jar
```

또는 production에서는 continuous recording으로:

```bash
-XX:StartFlightRecording=disk=true,maxage=1h,maxsize=200M,filename=app.jfr
```

이렇게 두면 JFR이 항상 돌면서 최근 1시간 또는 200MB까지의 이벤트를 디스크에 보관한다. 사고가 터지면 그 시점 직전의 데이터를 갖고 있다. JMC(Java Mission Control)에서 열어 `GC Pause` 이벤트를 본다. p99의 pause 길이가 어디서 튀는지, mixed collection이 길어지는 시점이 있는지 — 한눈에 보인다.

**Spring Boot Actuator의 메트릭과 결합.** `management.endpoints.web.exposure.include=health,info,metrics`를 켜두면 `/actuator/metrics/jvm.gc.pause`로 GC pause 분포를 가져올 수 있다. Micrometer가 Prometheus·Datadog로 보내면 Grafana 대시보드가 된다. *반드시 메트릭을 먼저 보고, 그 다음에 GC 옵션을 만지자*. 측정 없는 튜닝은 미신이다.

**일반적인 Spring Boot 권장 옵션 패턴.** 한 가지 시작점을 깔자면 이렇다.

```bash
-XX:MaxRAMPercentage=60
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+UnlockDiagnosticVMOptions
-XX:+LogVMOutput
-XX:StartFlightRecording=disk=true,maxage=1h,maxsize=200M,filename=/tmp/app.jfr,settings=profile
-Xlog:gc*:file=/tmp/gc.log:time,uptime,level,tags:filecount=10,filesize=50M
```

이게 모든 케이스의 답은 아니다. 그러나 *side effect가 적고 진단이 잘 되는* 시작점이다. heap은 cgroup limit의 60%로 자동 조절, G1으로 default 유지, GC pause 목표 200ms, JFR과 GC log를 디스크에 회전 저장. 사고가 터지면 데이터가 있다.

*권장하지 않는 패턴.* "`-XX:+UseStringDeduplication`을 항상 켜라", "`-XX:+ParallelRefProcEnabled`를 꼭 켜라" 같은 인터넷 블로그의 마법 주문들. 케이스에 따라 도움이 될 수도 있고 해가 될 수도 있다. *측정 없이 켜지 말자*.

## 메모리의 두 얼굴 — GC와 JMM 사이의 다리

이 장의 끝에서 한 번 멈춰 서서, 우리가 놓치고 가는 것을 짚어야 한다. 자바의 "메모리"는 사실 *두 얼굴*을 갖고 있다.

하나는 우리가 이 장에서 본 얼굴이다. heap, region, generation, pause, footprint. *물리적 메모리의 관리* — 어떤 객체를 어떤 영역에 두고, 어떻게 회수할 것인가. GC가 답하는 영역이다. 11년 동안 우리는 이 얼굴을 ZGC와 Generational Shenandoah까지 끌고 왔다. sub-ms pause라는 결과를 손에 쥐었다.

다른 하나는 **Java Memory Model**(JMM)이 그리는 얼굴이다. happens-before, volatile, final field semantics, synchronization order. *동시성 의미론으로서의 메모리* — 한 스레드의 쓰기가 다른 스레드에 *언제, 어떤 순서로* 보이는가. 8A장에서 우리가 만났던 그 영역이다. JLS §17.4가 명시하는 그 모델이다. JSR-133이 2004년에 풀어낸 그 약속이다.

이 두 얼굴은 자주 따로 다뤄진다. GC 튜닝하는 사람은 JMM을 잘 모르고, JMM을 다루는 사람은 GC 옵션에 무관심하다. 그러나 *둘은 한 메모리의 두 얼굴*이다. ZGC가 colored pointer로 객체를 옮겨도, 그 이동이 다른 스레드에 일관되게 보이려면 JMM의 happens-before가 받쳐줘야 한다. G1의 region 압축이 일어나는 동안 volatile read는 여전히 정확한 값을 봐야 한다. GC와 JMM은 *같은 메모리*에 대해 서로 다른 층위의 약속을 한다. 한 층은 *얼마나 빨리 회수하느냐*를, 다른 층은 *어떤 순서로 보이느냐*를 보장한다.

우리가 ZGC의 sub-ms pause를 신뢰할 수 있는 이유는, 그 GC가 JMM의 약속을 깨지 않기 때문이다. 11년의 GC 진화는 *JMM의 약속을 지키면서* throughput과 latency를 동시에 끌어올린 과정이었다. 8A장의 JMM과 이 장의 GC는 *한 메모리 위에서 함께 움직인다*. 둘 중 하나만 알면 절반만 아는 것이다.

다음 장에서는 그 메모리의 한 단계 *더 바깥*으로 나가본다. heap 안의 객체가 아니라, *heap 밖의 native memory*를 자바가 어떻게 다루게 됐는지. JNI에 시달리던 우리가 FFM과 만나는 그 자리다. 자바가 SIMD를 *표현*할 수 있게 된 그 자리다. ASM이 더 이상 필요 없게 된 그 자리다.

함께 걸어보자.
