# 8A장. j.u.c와 Java Memory Model — 동시성의 토대

단일 인스턴스에서 잘 돌던 코드가 멀티 코어에서 깨졌다고 해보자.

재고 차감 로직이다. 주문이 들어오면 `Stock.count`를 하나 깎고 DB에 반영한다. 통합 테스트는 통과했다. QA 환경에서도 문제없었다. 그런데 운영 단일 노드에 코어 16개짜리 머신을 박고 부하 테스트를 돌렸더니, 5만 건 주문에 재고가 0으로 떨어져야 할 자리에서 *마이너스 23*이 찍혀 있다. 로그를 봐도 예외는 없다. 트랜잭션 격리 수준은 `READ_COMMITTED`로 맞춰 뒀고, JPA의 1차 캐시도 의심해 봤다. 결국 문제는 자바 코드의 가장 평범해 보이던 한 줄이었다.

```java
public class Stock {
    private int count;
    public void decrement() { count--; }
}
```

`count--` 한 줄이 무엇이 문제일까? 그것은 *하나의 연산이 아니다.* 읽고, 빼고, 쓰는 세 단계다. 게다가 그 세 단계 사이에 다른 스레드가 끼어들 수 있다는 것보다 더 무서운 사실이 있다 — *내가 쓴 값이 다른 스레드의 시야에 영원히 도달하지 않을 수도 있다.* 메모리 모델이라는 단어를 처음 들어본 사람에게 이 문장은 거의 협박처럼 들린다. 그러나 자바 동시성의 모든 것은 정확히 이 한 문장에서 출발한다.

이 장에서는 우리가 매일 쓰던 `synchronized`와 `volatile`이 *정확히 무엇을 보장하는지*, 그리고 그 보장의 근거가 되는 Java Memory Model(JMM)이 어떤 모양인지를 들여다본다. JSR 133이라는 무거운 이름의 문서를 회피하지 말자. 이 문서를 한 번 정독한 개발자는 그렇지 않은 개발자와 동시성 코드를 짤 때 완전히 다른 사람이 된다. 그러고 나면 `java.util.concurrent`(이하 j.u.c) 패키지가 *왜 그 모양으로* 설계됐는지가 비로소 보이기 시작한다.

## 메모리 모델은 *왜* 필요한가

먼저 한 가지 오해부터 풀자. JMM은 "JVM이 메모리를 어떻게 배치하는가"에 대한 명세가 *아니다.* JMM은 **여러 스레드가 공유 변수에 행한 읽기·쓰기가 서로에게 어떤 순서로 보이는가**를 규정하는 명세다. 더 정확히 말하면, *어떤 순서로 보일 수 있는지*에 대한 *제약*이다.

왜 이런 제약이 필요한가? 두 가지 현실 때문이다.

첫째, **CPU는 명령어를 재정렬한다.** 현대 CPU는 파이프라인을 비우지 않으려고 의존성 없는 명령어 순서를 자유롭게 바꾼다. 같은 코어의 store buffer는 쓰기를 지연시킬 수 있고, 인접 코어의 캐시는 무효화 메시지를 받기 전까지 오래된 값을 들고 있을 수 있다.

둘째, **JIT 컴파일러도 재정렬한다.** HotSpot은 escape analysis, loop hoisting, dead store elimination 같은 최적화를 수행한다. 그 결과로 소스 코드의 순서와 실제 실행 순서는 별개가 된다.

그렇다면 어떻게 해야 할까? 두 가지 길이 있다. 하나는 *모든 재정렬을 금지*하는 것이다. 그러면 멀티 코어의 성능 이점이 거의 사라진다. 다른 하나는 *프로그래머가 명시한 곳에서만* 재정렬을 제한하는 것이다. 이쪽이 자바가 택한 길이다. JMM은 "프로그래머가 약속한 곳"의 모양을 happens-before라는 관계로 정의한다.

## happens-before — 동시성 코드의 단 하나의 문법

happens-before는 두 액션 A와 B 사이의 *관계*다. "A가 B보다 시간상 먼저 일어났다"가 아니다 — "A의 결과를 B가 *반드시* 볼 수 있다"는 *보증*이다. 시간이 아니라 *가시성*이다.

JLS §17.4.5는 이 관계를 다음과 같이 규정한다.

> **JLS §17.4.5 (Happens-before Order) — 원문 박스**
>
> *"Two actions can be ordered by a happens-before relationship. If one action happens-before another, then the first is visible to and ordered before the second."*
>
> **번역**: 두 액션은 happens-before 관계로 순서가 지어질 수 있다. 만약 한 액션이 다른 액션보다 happens-before 관계라면, 앞 액션은 뒤 액션에게 *가시적*이고 *순서가 보장된다*.
>
> **해설**: 핵심 단어는 *visible*이다. happens-before는 단순한 순서가 아니라 가시성을 약속한다. A가 쓴 값을 B가 반드시 *볼 수 있다*는 보증이며, A의 모든 쓰기(공유 변수든 아니든)가 B 시점에는 메모리에 반영돼 있다는 약속이다.
>
> **본문 연결**: 그러므로 우리가 `volatile`·`synchronized`·`Thread.join`을 쓰는 진짜 이유는 락이 아니라 *가시성을 만드는 일*이다. 락을 잡는 것은 부수 효과일 뿐이다.

happens-before 관계를 만들어 내는 *생성자*들은 정해져 있다. 일곱 가지다.

1. **Program order rule**: 같은 스레드 내에서, 소스 코드 순서대로 happens-before.
2. **Monitor lock rule**: 같은 락에 대한 `unlock`은 그 다음 `lock`보다 happens-before.
3. **Volatile variable rule**: 같은 volatile 변수에 대한 `write`는 그 다음 `read`보다 happens-before.
4. **Thread start rule**: `Thread.start()` 호출은 그 스레드 안의 모든 액션보다 happens-before.
5. **Thread termination rule**: 스레드 안의 모든 액션은 다른 스레드의 `Thread.join()` 반환보다 happens-before.
6. **Interruption rule**: `Thread.interrupt()` 호출은 인터럽트 감지보다 happens-before.
7. **Finalizer rule**: 객체의 생성자 종료는 finalizer 시작보다 happens-before.

그리고 마지막으로 **transitivity** — A → B이고 B → C이면 A → C다. 이 추이성이 실무에서 가장 중요하다. 한 스레드가 volatile 변수에 *플래그* 하나만 쓰면, 그 스레드가 그전에 일반 변수에 쓴 모든 값이 *동시에* 다른 스레드에 가시적이 된다. 플래그 하나에 *모든 쓰기*가 묶여 따라간다는 뜻이다. 이걸 모르고 동시성 코드를 짜면, 디버깅이 거의 불가능한 미스터리에 빠진다.

## volatile은 *정확히* 무엇을 보장하는가

`volatile`을 두고 "최신 값을 보장한다"라거나 "캐시를 무효화한다"라고 설명하는 글이 많다. 둘 다 잘못된 비유다. 정확한 정의는 위의 *volatile variable rule* 한 줄이다 — **같은 volatile 변수에 대한 write는 그 다음 read보다 happens-before**.

여기서 두 가지 함의가 따라온다. 첫째, volatile read는 동기화 진입(`acquire`)과 같은 효과를 낸다. 그 read 이후에 오는 모든 일반 read는 *이전 스레드의 모든 쓰기*를 본다. 둘째, volatile write는 동기화 종료(`release`)와 같은 효과를 낸다. 그 write 이전에 한 모든 일반 write는 *다음 스레드의 어떤 read*에서도 가시적이 된다.

그렇다면 `volatile`로 무엇이 가능하고 무엇이 *불가능*한가?

**가능한 것**: 상태 플래그, 더블 체크 아이디엄의 안전화, lock-free 카운터에 *최신 값 읽기*.

**불가능한 것**: `count++` 같은 *read-modify-write* 연산의 원자성. 왜냐하면 그것은 *세 액션*이지 하나의 액션이 아니기 때문이다. volatile은 *원자성*을 주지 않는다. 원자성은 다른 도구의 영역이다.

```java
private volatile int count;
public void inc() { count++; } // ❌ 여전히 race condition
```

이 코드가 *어떻게* 깨지는지는 자명하다. 두 스레드가 동시에 `count=5`를 읽고, 둘 다 6을 쓰면, 결과는 7이 아니라 6이다. volatile은 *가시성*만 주지 *원자성*은 주지 않는다는 사실을 잊지 말자.

## synchronized와 락의 두 얼굴

`synchronized`는 두 가지 일을 *동시에* 한다. 하나는 **상호 배제**(mutual exclusion) — 같은 락을 잡은 다른 스레드를 막는다. 다른 하나는 **가시성** — `unlock`은 그 다음 같은 락의 `lock`보다 happens-before다. 자바에서 *동시성 도구의 모든 보장*은 이 두 얼굴의 조합으로 만들어진다.

흔한 오해 하나. "단일 스레드만 들어가니까 가시성 문제는 자동으로 풀린다"고 생각하기 쉽다. 정반대다. *상호 배제가 가시성을 만드는 것이 아니라*, synchronized의 happens-before 효과가 가시성을 만든다. 같은 락이라는 점이 핵심이다 — *다른* 락이면 happens-before가 성립하지 않는다.

예제로 보자. 흔한 더블 체크 락킹(double-checked locking, DCL)이다.

```java
public class Holder {
    private static Holder instance;
    public static Holder getInstance() {
        if (instance == null) {              // (1)
            synchronized (Holder.class) {
                if (instance == null) {      // (2)
                    instance = new Holder(); // (3)
                }
            }
        }
        return instance;                     // (4)
    }
}
```

이 패턴은 Java 5 이전까지 *깨진 코드*였다. (3)에서의 객체 생성은 ① 메모리 할당, ② 생성자 실행, ③ 참조 대입의 세 단계로 나뉘는데, JVM이 ②와 ③의 순서를 바꿔도 무방한 시절이 있었다. 다른 스레드가 (1)에서 `instance != null`을 보고 (4)에서 *아직 생성자가 끝나지 않은* 객체를 들고 가는 사태가 가능했다. *끔찍한 일이다.*

Java 5에서 JSR 133이 도입되면서 해법이 생겼다. `instance`를 `volatile`로 선언하면 (3)의 모든 write가 다음 스레드의 (1) read에 가시적이 된다. happens-before가 *전이적으로* 생성자 안의 모든 필드까지 따라가 준다.

```java
private static volatile Holder instance; // Java 5+에서 이 한 줄로 해결
```

이 패턴은 지금도 동작한다. 그러나 더 명확한 대안이 있다 — *holder idiom*이다.

```java
public class Holder {
    private Holder() {}
    private static class Lazy { static final Holder INSTANCE = new Holder(); }
    public static Holder getInstance() { return Lazy.INSTANCE; }
}
```

내부 클래스의 `static final` 필드는 클래스 초기화 시점에 단 한 번 초기화되며, JVM이 그 초기화에 동기화를 보장한다. 더 단순하고, 더 빠르고, *읽는 사람이 즉시 이해한다.* DCL은 역사적으로 의미가 있지만, 실무에서는 이쪽을 *기억해두는 편이 낫다.*

## final 필드의 특별한 약속

JMM에는 *final 필드만을 위한* 별도의 보증이 있다. JLS §17.5다.

> **JLS §17.5 (final Field Semantics) — 원문 박스**
>
> *"The usage model for final fields is a simple one: Set the final fields for an object in that object's constructor; and do not write a reference to the object being constructed in a place where another thread can see it before the object's constructor is finished."*
>
> **번역**: final 필드의 사용 모델은 단순하다. 객체의 생성자 안에서 final 필드들을 초기화하라. 그리고 *생성자가 끝나기 전*에 그 객체의 참조를 다른 스레드가 볼 수 있는 곳에 *써넣지 말라.*
>
> **해설**: 이 약속을 지키면 JMM은 *동기화 없이도* final 필드의 초기값이 모든 스레드에 가시적임을 보장한다. 단, 약속을 지킨 객체에 한해서다.
>
> **본문 연결**: 우리가 `String`·`Integer`·records를 자유롭게 공유하는 이유가 여기에 있다. 그들의 모든 상태는 final이고, 생성자가 끝나기 전에 *this 참조가 새지 않으면* 가시성은 공짜로 따라온다.

여기서 *생성자가 끝나기 전에 this 참조가 새는 일*을 **safe publication 위반**이라 부른다. 흔한 예가 생성자 안에서 리스너에 자기 자신을 등록하는 경우다. 그 순간 *반쯤 초기화된 객체*가 외부에 노출된다. 이건 final 필드의 보증도 깨뜨린다. *난감하다.* 해결은 단순하다 — 등록은 생성자 밖에서, 별도의 초기화 메서드에서 하자.

이것이 records가 동시성에서 *그토록 편한* 이유이기도 하다. records의 컴포넌트는 모두 final이고 canonical constructor가 강제된다. safe publication만 지키면 멀티 스레드에서 공유해도 *동기화 없이도* 안전하다. 자바가 마침내 "값"이라는 신원을 인정한 그 결과다.

## out-of-thin-air — JMM이 *허용하지 않는* 한 가지

JMM의 행동 정의에는 한 가지 묘한 구멍이 있다. 순수 happens-before 모델은 *허공에서 솟아난 값(out-of-thin-air, OOTA)*을 허용해 버린다는 점이다. 예를 들어 두 스레드가 서로의 변수를 읽어 자기 변수에 쓴다고 해보자. 만약 둘 다 "상대가 42를 쓸 거니까 나도 42를 쓰자"고 *예측*해서 정합성 있게 끝맺는 실행이 존재한다면, happens-before만으로는 이를 금지하지 못한다.

물론 실제 JVM은 OOTA 값을 만들지 않는다. JMM 명세는 happens-before 위에 **causality requirements**라는 별도의 well-formed execution 정의를 얹어 이런 실행을 *명시적으로 배제*한다. 실무 개발자가 이 사실을 매일 의식할 필요는 없다 — 그러나 메모리 모델 명세가 그저 happens-before 한 줄로 끝나지 *않는다는* 사실은 기억해두자. 동시성은 직관보다 깊다.

## j.u.c — Doug Lea가 세운 도시

JMM이 *문법*이라면, `java.util.concurrent`는 그 문법으로 지어진 *도시*다. 2004년 Java 5에 JSR 166으로 도입된 이래, Doug Lea를 비롯한 EG는 모든 락·큐·실행자·atomic·sync 도구를 *JMM 위에서 안전한 형태로* 구현해 두었다. 우리가 더 이상 `wait/notify`를 직접 만질 일이 없는 이유다.

**Atomic 패키지** — `AtomicInteger`, `AtomicLong`, `AtomicReference`. CAS(compare-and-swap) 명령어 한 번으로 read-modify-write를 원자화한다. `count.incrementAndGet()`은 위에서 본 `count++`의 깨진 버전을 한 줄로 고친다. 내부적으로는 `Unsafe.compareAndSwapInt` 호출이며, 실패 시 spin retry한다. Java 8에서 `LongAdder`·`LongAccumulator`가 추가됐는데, *많은 스레드의 누적 합산*에서 `AtomicLong`을 한참 앞서는 성능을 보인다. 핵심 차이는 *셀 분산*이다 — 단일 변수가 아니라 스레드별 셀에 누적해 두고, 읽을 때만 합산한다. 카운터·통계·로깅 누적에는 `LongAdder`를 *기억해두자.*

**락 패키지** — `ReentrantLock`은 `synchronized`의 모든 보장을 그대로 주면서 `tryLock`, `lockInterruptibly`, fair 정책, 다중 `Condition`을 추가로 제공한다. Java 8 이전엔 성능 이점도 있었지만, HotSpot의 biased lock·thin lock 최적화로 `synchronized`도 충분히 빨라졌다. 지금은 *기능적 필요*가 있을 때 `ReentrantLock`을 쓰자.

`ReadWriteLock`은 *읽기 다수, 쓰기 소수*인 캐시류에서 빛난다. 그러나 read 락 자체가 cache line bouncing을 만들기에, 진짜 read-heavy 워크로드에서는 *immutable한 스냅샷 + AtomicReference 교체*가 더 빠를 때가 많다.

Java 8에 추가된 `StampedLock`은 *optimistic read*라는 새 모드를 추가했다 — 락을 잡지 *않고* 읽은 뒤, 끝에서 stamp가 여전히 유효한지만 검증한다. read 비용이 사실상 volatile read 수준이다. 다만 reentrant가 *아니고* `Condition`도 없다. 강력한 무기지만 잘못 쓰면 손가락을 자른다.

**BlockingQueue 계열** — `ArrayBlockingQueue`(고정 크기), `LinkedBlockingQueue`(가변), `SynchronousQueue`(0 용량 핸드오프), `PriorityBlockingQueue`(우선순위), `DelayQueue`(지연 발행), `LinkedTransferQueue`(transfer 시맨틱). Producer-consumer 패턴의 표준 도구다. `put`·`take`는 happens-before를 만든다 — 즉, 큐에 객체를 넣은 시점까지의 모든 쓰기가 꺼낸 쪽에 가시적이다.

**ConcurrentHashMap의 내부 진화** — Java 7까지는 segment lock(16개의 부분 락)이었다. Java 8에서 *완전히 다시 썼다.* 버킷 단위 CAS + `synchronized` block, 충돌이 8개를 넘으면 linked list가 *red-black tree*로 자동 승격(O(n) → O(log n)). `compute`·`merge`·`computeIfAbsent`가 추가됐고, `forEach`·`reduce`·`search`로 병렬 처리가 가능하다. `size()`도 `LongAdder` 스타일로 분산 셀에 누적한다. 옛 segment lock의 read-write 컨텐션 문제가 거의 사라졌다. *모던 자바의 가장 중요한 자료구조 한 가지*를 꼽으라면 이쪽이다.

**동기화 보조 — `CountDownLatch`, `CyclicBarrier`, `Semaphore`, `Phaser`**. 각각 일회용 카운트다운, 재사용 가능한 배리어, 카운팅 세마포어, 동적 단계 진행 도구다. `Phaser`는 다소 복잡하지만, 단계별로 *참가자가 동적으로 변하는* 시뮬레이션·테스트 시나리오에서 강력하다.

## ForkJoinPool과 work-stealing — 그리고 commonPool의 함정

Java 7에서 도입된 `ForkJoinPool`은 *분할 정복형 CPU-bound 작업*을 위한 풀이다. 각 워커 스레드가 자기 deque를 갖고, deque가 비면 *다른 워커의 deque 꼬리를 훔쳐* 일을 가져온다(work-stealing). idle 워커가 알아서 짐을 나누니, 작업 분배 로직을 짤 필요가 없다. `RecursiveTask`·`RecursiveAction`을 상속해서 `compute()`에 분할 로직을 적으면 끝이다.

그리고 Java 8에서 `ForkJoinPool.commonPool()`이라는 *전역 공용 풀*이 도입됐다. 기본 스레드 수는 `availableProcessors() - 1`. 이 풀은 다음 세 가지가 *모두* 공유한다.

- `parallelStream()`
- `CompletableFuture.supplyAsync(...)`의 *executor 인자 없는 호출*
- `ForkJoinPool.commonPool().submit(...)`

여기서 *끔찍한 일이* 시작된다. 가령 이런 코드를 보자.

```java
ordersStream.parallel()
    .map(order -> paymentClient.charge(order)) // HTTP 호출, blocking
    .toList();
```

이 코드는 *commonPool에 blocking I/O를 태운다.* 워커가 HTTP 응답을 기다리는 동안 풀은 비어 있고, 같은 JVM의 다른 모든 `parallelStream`·`CompletableFuture`가 *함께 굶는다.* p99 latency가 일정하지 않게 폭주하는 흔한 원인이다. 이 사실을 모르는 팀은 "왜 parallelStream을 켰는데 더 느려졌지?"를 반나절 헤매다 결국 `parallel()`을 떼는 것으로 끝난다.

해법은 단순하다. **commonPool에는 CPU-bound 작업만 태우자.** Blocking I/O는 별도의 풀 — `Executors.newFixedThreadPool` 또는 (Loom 시대라면) virtual thread per task executor — 로 보낸다. `CompletableFuture`라면 *항상 executor를 명시적으로 지정*하는 편이 낫다. 그게 안전하다.

여기서 한 가지 미리 짚어두자. 이 모든 풀과 락의 *진짜 가치*는 Part VII의 Loom 시대에 다시 따져봐야 한다. virtual thread가 *thread-per-request*를 다시 합리적으로 만든 순간, "thread pool은 비싸니까 재사용해야 한다"는 11년의 통념이 흔들리기 시작한다. 그러나 지금은 그 이전의 세계를 정직하게 마주하는 일이 먼저다.

## Spring 맥락 — 1차 캐시와 ThreadLocal

JPA의 `EntityManager`는 thread-safe하지 *않다.* 1차 캐시(영속 컨텍스트)는 단일 스레드에 *confined*된다는 전제다. Spring의 `OpenEntityManagerInView` 패턴은 요청 스레드에 `EntityManager`를 묶어두는 것으로 이 전제를 지킨다. `@Transactional` 메서드의 가시성 보장도 같은 토대 위에 있다 — 트랜잭션 진입과 종료가 JDBC connection의 commit/rollback에 묶이고, JDBC 드라이버가 그 시점에서 가시성을 만들어 준다.

`@Scope("prototype")`과 `singleton`의 차이도 이 맥락에서 다시 보자. singleton Bean이 *상태를 들고 있다면* 자동으로 멀티 스레드에 노출된다. 그 상태가 *가변*이라면 동기화가 필요하다. 가장 흔한 함정은 `private SimpleDateFormat sdf`를 singleton 서비스 Bean에 박아두는 일이다. `SimpleDateFormat`은 thread-safe하지 않다. `DateTimeFormatter`(Java 8, immutable)로 바꾸자 — 그게 *훨씬 낫다.*

ThreadLocal Bean도 한 번 들여다볼 만하다. ThreadLocal은 thread-confined를 강제해 가시성 문제를 회피하는 도구지만, 자체로 *위험한 도구*다. 풀에서 재사용되는 스레드에 ThreadLocal이 남아 있으면, *다음 요청이 이전 요청의 상태를 본다.* Spring Security의 `SecurityContextHolder`가 잘 알려진 사례 — request 끝에 반드시 `clear()`해야 한다. virtual thread 시대에는 이 패턴 자체가 흔들린다는 점도 *기억해두자.* Scoped Values라는 후속 도구가 16장에서 등장한다.

## 마무리

이 장에서 우리는 자바 동시성의 *문법책*을 펼쳤다. happens-before라는 단 하나의 관계가 volatile·synchronized·final·Thread.start·Thread.join을 한 줄로 묶고, j.u.c의 모든 도구가 그 문법 위에서 안전하게 작동한다는 사실을 확인했다. CAS·work-stealing·tree-bin 같은 구현 기법들도 결국 happens-before를 깨지 않으면서 성능을 회복하는 도구들이었다.

이제 문법은 갖춰졌다. 그러나 비동기 *조합*은 또 다른 이야기다. 외부 API 세 개를 *병렬로* 호출하고, 그중 하나가 실패했을 때 우아하게 복구하고, 그 결과를 다시 *순차적으로* 합쳐 클라이언트에 돌려주는 일 — `Future` 하나로는 어림없다. 다음 장에서는 `CompletableFuture`가 어떻게 콜백 지옥에서 우리를 꺼냈고, Java 9의 `Flow`가 어떻게 그 흐름을 또 한 번 일반화했는지 살펴보자. 그 끝에서 우리는 Reactive Streams라는 이름의 길고 험한 산을 만난다.
