# 18장. Foreign Function & Memory API · Vector API · Class-File API

JNI `*.h` 추출에 하루를 통째로 쓴 그날을 기억하는가.

`zlib`을 자바에서 호출하고 싶었을 뿐이다. 그런데 일은 그렇게 단순하지 않았다. 먼저 `native` 메서드를 자바 코드에 선언한다. 그 다음 `javac`로 컴파일하고, `javah`로(또는 Java 8 이후엔 `javac -h`로) `.h` 헤더를 추출한다. 헤더에 적힌 `JNIEXPORT void JNICALL Java_com_example_Zlib_compress(JNIEnv *, jobject, jbyteArray)` 같은 길고 추한 시그니처를 보고 잠시 한숨을 쉰다. `.c` 파일에서 그 시그니처를 구현하는데, `(*env)->GetByteArrayElements`로 자바 배열을 C 배열로 끌어내고, 다 쓰면 `ReleaseByteArrayElements`로 풀어줘야 한다. 잊으면? 메모리 누수다. 잘못 푸는 순서를 짜면? *JVM 전체가 죽는다*.

그러고도 끝이 아니다. `gcc -shared -fPIC`로 `.so`를 빌드하고(Windows라면 `.dll`, Mac이라면 `.dylib`), `System.loadLibrary("zlib_wrapper")`로 자바가 그걸 찾을 수 있게 해야 한다. CI에서 빌드할 때 native toolchain이 자동으로 깔려 있어야 하고, 배포 환경의 glibc 버전과 빌드 환경의 glibc 버전이 안 맞으면 또 죽는다. 컨테이너에 native shared library를 같이 패키징해야 하고, ARM과 x64 양쪽 빌드를 따로 굴려야 한다. *번거롭다*는 말로 부족하다. *끔찍한 일이다*.

이 모든 것이 — 우리는 그저 `zlib`의 `compress` 함수를 자바에서 부르고 싶었을 뿐이다.

JNI에 시달려본 사람이라면, JNI가 *왜 끝나야 했는지* 굳이 설명할 필요가 없다. 그러나 끝났다는 *증거*는 필요하다. 진짜로 끝났는가? 자바는 이제 `*.h` 없이 native를 부를 수 있는가? 그리고 — *그것만으로는 부족하다*. 우리는 또 두 가지 질문을 동시에 던지고 있다. "자바는 SIMD를 어떻게 표현하는가?", "ASM·BCEL로 바이트코드를 생성하던 그 *부족 비밀*은 이제 무엇으로 대체되는가?"

이 세 질문이 한 장에 모인 이유는 분명하다. 세 변화 모두 *Project Panama*의 깃발 아래에서 진행됐고, 셋 모두 자바를 "native ecosystem과 더 가깝게" 가져가려는 한 흐름의 다른 얼굴이다. 함께 살펴보자.

## §18.1 FFM — JNI 시대의 종료

**Foreign Function & Memory API**의 여정을 한 줄로 요약하면 이렇다. Java 14의 incubator에서 Java 22의 표준으로, 8년에 걸친 점진적 진화.

| JEP | Java | 단계 |
|---|---|---|
| 370 | 14 | Foreign-Memory Access API (Incubator) |
| 412 | 17 | Foreign Function & Memory API (Incubator) — 17 LTS에 들어옴 |
| 419 | 18 | Second Incubator |
| 424 | 19 | Preview |
| 434 | 20 | Second Preview |
| 442 | 21 | Third Preview — 21 LTS에 들어옴 |
| **454** | **22** | **Standard** — JNI 시대 종료의 시작 |

이 9개 릴리스에 걸친 점진성이 자바의 진화 방식을 잘 보여준다. *서두르지 않는다*. preview에서 incubator에서 standard로 가는 동안 API 표면이 다듬어지고, 8년 후에 표준이 된다. 그 결과로 우리 손에 들어온 추상은 깔끔하다. 핵심 다섯 개만 짚어보자.

### MemorySegment — native memory의 일급 추상

`MemorySegment`는 *어딘가에 존재하는 메모리 영역*을 표현한다. heap일 수도 있고, native memory일 수도 있고, mapped file일 수도 있다. 어디에 있든 `MemorySegment` 하나로 다루는 것이 핵심이다.

```java
MemorySegment segment = arena.allocate(100); // native memory 100바이트
segment.set(ValueLayout.JAVA_INT, 0, 42);    // offset 0에 int 42 쓰기
int value = segment.get(ValueLayout.JAVA_INT, 0); // 읽기
```

`set`/`get`은 `ValueLayout`을 받는다 — `JAVA_INT`, `JAVA_LONG`, `JAVA_DOUBLE` 같은 primitive layout이거나, `ADDRESS`(포인터)이거나, 또는 우리가 직접 정의한 `StructLayout`이다. C의 `struct sockaddr_in` 같은 구조체를 자바에서 그대로 표현할 수 있다. *기억해두자*. JNI 시절에는 `Get*ArrayElements`로 자바 배열을 native 쪽에서 빌려와야 했지만, FFM은 그 경계 자체가 사라졌다.

### Arena — lifetime 관리의 핵심

native memory의 가장 어려운 문제는 *언제 해제할 것인가*다. 너무 일찍 해제하면 use-after-free, 너무 늦으면 누수. C 프로그래머가 평생 씨름하는 그 문제. FFM은 `Arena`로 이 문제를 try-with-resources의 영역으로 끌어왔다.

```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment segment = arena.allocate(100);
    // segment 사용
} // arena가 닫히면서 segment 자동 해제
```

`Arena`에는 세 가지 종류가 있다.

- **`Arena.ofConfined()`**: 한 스레드 안에서만 쓸 수 있다. 다른 스레드가 접근하면 즉시 예외. 가장 빠르고 가장 안전하다. 대부분의 경우 이걸 쓰는 편이 낫다.
- **`Arena.ofShared()`**: 여러 스레드에서 공유한다. 그 대신 약간의 동기화 비용. 동일 native 리소스를 여러 worker에서 접근해야 할 때.
- **`Arena.ofAuto()`**: GC가 해제 시점을 결정한다. C의 `malloc`처럼 들고 다니다가, 더 이상 참조되지 않으면 자동 해제. 가장 자바스럽지만, *정확한 해제 시점이 보장되지 않는다*는 함정이 있다. 즉시성이 필요하면 confined나 shared를 쓰자.

이 세 가지 lifetime 모델은 단순한 API 디자인이 아니다. JNI에서 *완전히 빠져 있던* 안전망이다. JNI는 누가 언제 메모리를 풀어줄지 약속하지 않았다. FFM은 그 약속을 try-with-resources의 문법으로 못 박는다. 누수와 use-after-free는 *컴파일러가 아니라 런타임이 잡아준다*. confined arena에 다른 스레드가 접근하면 `WrongThreadException`이 즉시 떨어진다. 침묵하는 메모리 손상이 아니라 *시끄러운 실패*다.

### Linker — C 함수의 호출

native 메모리만으로는 부족하다. C 함수를 *불러야* 한다. `Linker`가 그 일을 한다.

```java
Linker linker = Linker.nativeLinker();
SymbolLookup stdlib = linker.defaultLookup();
MemorySegment strlenAddr = stdlib.find("strlen").orElseThrow();

MethodHandle strlen = linker.downcallHandle(
    strlenAddr,
    FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
);

try (Arena arena = Arena.ofConfined()) {
    MemorySegment cStr = arena.allocateUtf8String("Hello, FFM");
    long len = (long) strlen.invoke(cStr);
    System.out.println(len); // 10
}
```

세 단계다. *어디에 있는지 찾고*(`SymbolLookup.find`), *시그니처를 적고*(`FunctionDescriptor`), *MethodHandle을 얻어서 부른다*. `FunctionDescriptor.of(returnType, argTypes...)`는 C 함수의 시그니처를 자바 쪽 표현으로 옮긴 것이다. `strlen`은 `size_t strlen(const char *)`이니 return은 `JAVA_LONG`, arg는 `ADDRESS`.

이게 JNI의 `Java_com_example_...` 시그니처를 직접 적던 시절과 비교가 되는가? 자바 코드 안에서 *자바 문법으로* C 함수의 시그니처를 표현한다. `.h` 헤더도, `.c` 구현도, `gcc` 빌드도, `loadLibrary`도 필요 없다. `defaultLookup()`이 libc의 함수를 찾아주고, 우리 라이브러리라면 `SymbolLookup.libraryLookup(path, arena)`로 `.so`를 직접 열 수 있다.

### jextract — 헤더 자동 바인딩

그런데 — 정직하게 짚자. 위의 `Linker` 코드를 *모든 함수마다 손으로 적는 일*은 여전히 *번거롭다*. `zstd` 라이브러리에 함수가 100개라면? 100번을 적는가? 그건 JNI 시대와 다를 게 없다.

이 자리에 **jextract**가 들어선다. C 헤더 파일을 입력으로 받아 자바 바인딩을 자동 생성한다.

```bash
jextract --output src/main/java \
         -t com.example.zstd \
         /usr/include/zstd.h
```

이 한 줄로 `zstd.h`의 모든 함수·struct·constant가 자바 클래스로 풀린다. 우리가 손에 쥐는 건 `com.example.zstd.zstd_h.ZSTD_compress(...)` 같은 깔끔한 static 메서드들이다. C struct는 자바의 `StructLayout`으로 풀리고, constant는 자바 static 필드가 된다. `-l zstd` 옵션을 주면 `loadLibrary` 호출까지 코드에 묻혀 나온다.

JNI 시대의 하루치 작업이 *5분으로* 줄어든다. 과장이 아니다.

### 예제 — JNI에서 FFM으로

이론은 충분하니, 실제 ZNI 코드가 FFM으로 어떻게 갈아끼워지는지 한 번 보자. 압축 라이브러리 `zstd`를 부르는 코드.

**JNI 시대 (~50줄의 native + 자바 양쪽 코드)**

```java
public class ZstdJni {
    static { System.loadLibrary("zstd_wrapper"); }
    public native byte[] compress(byte[] input);
}
```

```c
// ZstdJni.c
#include <jni.h>
#include <zstd.h>

JNIEXPORT jbyteArray JNICALL
Java_com_example_ZstdJni_compress(JNIEnv *env, jobject this, jbyteArray input) {
    jsize len = (*env)->GetArrayLength(env, input);
    jbyte *src = (*env)->GetByteArrayElements(env, input, NULL);
    size_t bound = ZSTD_compressBound(len);
    jbyteArray result = (*env)->NewByteArray(env, bound);
    jbyte *dst = (*env)->GetByteArrayElements(env, result, NULL);
    size_t actual = ZSTD_compress(dst, bound, src, len, 3);
    (*env)->ReleaseByteArrayElements(env, input, src, JNI_ABORT);
    (*env)->ReleaseByteArrayElements(env, result, dst, 0);
    // actual로 jbyteArray 크기를 자르는 추가 작업 필요...
    return result;
}
```

`.h` 추출, `.c` 컴파일, `.so` 빌드, 배포 패키징, 플랫폼별 빌드 — 그 모든 작업이 코드 *바깥*에서 따라붙는다.

**FFM 시대 (jextract로 만든 바인딩 사용)**

```bash
jextract -lzstd -t com.example.zstd /usr/include/zstd.h
```

```java
import static com.example.zstd.zstd_h.*;

public class ZstdFfm {
    public byte[] compress(byte[] input) {
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment src = arena.allocate(input.length);
            MemorySegment.copy(input, 0, src, ValueLayout.JAVA_BYTE, 0, input.length);

            long bound = ZSTD_compressBound(input.length);
            MemorySegment dst = arena.allocate(bound);

            long actual = ZSTD_compress(dst, bound, src, input.length, 3);
            byte[] result = new byte[(int) actual];
            MemorySegment.copy(dst, ValueLayout.JAVA_BYTE, 0, result, 0, (int) actual);
            return result;
        }
    }
}
```

`.c`도, `.h`도, `gcc`도, `loadLibrary`도 없다. 자바 코드만 있다. lifetime은 `try-with-resources`로 명시. `WrongThreadException`이 잘못된 스레드 접근을 즉시 잡아준다. native가 crash해도 JVM 전체가 죽지 않는다 — FFM은 더 *안전한 경계*에서 호출한다.

**JNI는 정말 끝났는가?** 솔직히 답하자. *기존 코드는 여전히 JNI다*. 그리고 그 코드를 당장 갈아끼울 동기가 없을 수 있다. 그러나 *새로 짜는 native 호출은 더 이상 JNI를 쓸 이유가 없다*. Spring Boot 6 시대, Java 21 이상의 베이스라인에서 새 native 통합은 FFM이다. 암호화 라이브러리(libsodium, openssl), 압축(zstd, lz4), DB driver의 일부 hot path — 모두 FFM으로 옮겨 가고 있다. *권장형으로 말하자면*, JNI 코드를 새로 짤 생각이 든다면 한 번 멈춰 서서 FFM을 검토하는 편이 낫다.

## §18.2 Vector API — 자바가 SIMD를 표현하는 법

다음 질문으로 넘어가자. *자바는 SIMD를 어떻게 표현하는가?*

CPU에는 *SIMD*(Single Instruction Multiple Data) 명령이 있다. AVX2는 256비트 레지스터에 int 8개를 한 번에 곱하고, AVX-512는 512비트에 int 16개를 한 번에. ARM의 NEON·SVE도 같은 일을 한다. ML inference, 이미지 처리, 행렬 연산, 압축 — 모든 numeric loop가 SIMD로 *수 배에서 십수 배* 빨라진다.

그런데 — 자바에서 *어떻게* 표현하는가? 11년 전 답은 "*JNI로 C++ SIMD 라이브러리를 부른다*"였다. 또는 "*JIT의 auto-vectorization을 믿고 손은 안 댄다*". 둘 다 만족스러운 답이 아니다. JIT은 단순한 루프만 vectorize하고, JNI는 위에서 본 그 모든 비용을 짊어진다.

### Vector API의 9년 incubator

| JEP | Java | 단계 |
|---|---|---|
| 338 | 16 | First Incubator |
| 414 | 17 | Second Incubator |
| 417 | 18 | Third Incubator |
| 426 | 19 | Fourth Incubator |
| 438 | 20 | Fifth Incubator |
| 448 | 21 | Sixth Incubator |
| 460 | 22 | Seventh Incubator |
| 469 | 23 | Eighth Incubator |
| **489** | **24** | **Ninth Incubator** — *아직 표준 아님* |

9년째 incubator다. *왜 표준이 안 되는가?* 답은 단순하지 않지만 한 단어로 요약하면 **Valhalla**다. Project Valhalla의 value class(이전 이름 "inline class", "primitive class")가 들어오면, Vector API의 핵심 타입(`Vector`, `IntVector`, `FloatVector`)이 value class로 다시 설계돼야 한다. 지금 표준으로 굳히면 Valhalla가 들어왔을 때 backward incompatibility가 생긴다. 그래서 *기다리는* 중이다. 자바의 *서두르지 않는 진화*가 가장 길게 적용된 사례다.

### 핵심 API — VectorSpecies와 lane operation

Vector API의 코드 모양을 한 번 보자. 두 float 배열의 점곱(dot product).

```java
import jdk.incubator.vector.*;

public class DotProduct {
    static final VectorSpecies<Float> SPECIES = FloatVector.SPECIES_PREFERRED;

    public static float dot(float[] a, float[] b) {
        float sum = 0f;
        int i = 0;
        int upperBound = SPECIES.loopBound(a.length);
        FloatVector acc = FloatVector.zero(SPECIES);

        for (; i < upperBound; i += SPECIES.length()) {
            FloatVector va = FloatVector.fromArray(SPECIES, a, i);
            FloatVector vb = FloatVector.fromArray(SPECIES, b, i);
            acc = acc.add(va.mul(vb));
        }
        sum = acc.reduceLanes(VectorOperators.ADD);

        // 꼬리 처리 (배열 길이가 lane 수의 배수가 아닐 때)
        for (; i < a.length; i++) sum += a[i] * b[i];
        return sum;
    }
}
```

`VectorSpecies`가 핵심이다. `SPECIES_PREFERRED`는 *현재 CPU에서 가장 효율적인 lane 수*를 자동으로 고른다. AVX-512가 있으면 16, AVX2면 8, NEON이면 4. 코드는 한 번 짜고, JVM이 알아서 매핑한다. 같은 자바 코드가 x64에서는 AVX-512로, ARM에서는 NEON으로 컴파일된다. *이 추상이 자바 SIMD의 정체성이다*.

`fromArray`로 배열을 vector로 끌어오고, `mul`·`add`로 lane별 연산을 한 번에 한다. 256비트 vector라면 float 8개의 곱셈이 *한 명령*으로 끝난다. 마지막에 `reduceLanes(ADD)`로 lane들을 합산해 스칼라 결과를 얻는다.

성능 차이는 *워크로드에 따라* 2배~10배. ML inference의 inner loop, 이미지 필터의 컨볼루션, 압축 알고리즘의 hash, 암호화의 round function — 이런 hot path에서 효과가 두드러진다.

### 언제 쓰는가 — 그리고 언제 쓰지 말아야 하는가

Vector API는 *매력적이지만 만능이 아니다*. *주의해야 한다*. 몇 가지 함정.

**incubator라는 사실 자체.** `jdk.incubator.vector` 모듈에 들어 있고, 코드 빌드 시 `--add-modules jdk.incubator.vector --enable-preview`(릴리스에 따라) 같은 옵션이 필요하다. production에서 incubator API를 쓴다는 건 *다음 릴리스에서 API가 깨질 수 있다*는 약속을 받아들이는 일이다. 9년째 incubator이긴 하지만, 그 말은 9년째 *공식 안정성 보장이 없다*는 뜻이기도 하다.

**단순한 루프는 JIT이 알아서 한다.** `for (int i = 0; i < a.length; i++) c[i] = a[i] * b[i];`처럼 명백한 패턴은 HotSpot의 auto-vectorizer가 SIMD로 컴파일한다. Vector API를 직접 쓰는 이득이 없다. *측정해보고 쓰자*.

**Valhalla 이전의 박싱 비용.** 현재 Vector API의 vector 타입은 reference type이다. 자주 생성·소멸하면 allocation 비용이 따라붙는다. JIT의 escape analysis가 잘 박혀 들어가면 stack-allocated로 풀리지만, 그게 보장되지 않는다. *Valhalla의 value class가 들어와야 진정한 zero-cost*다.

**Spring에서의 자리.** 일반 Spring Boot 비즈니스 로직에는 Vector API의 자리가 거의 없다. 적합한 자리는 *극히 좁다* — 이미지 처리 마이크로서비스, ML inference 서버, 암호화 hot path, 압축 코덱. 만약 우리가 손으로 SIMD를 쓰고 싶을 만큼 numeric loop가 hot path에 있다면 그제야 검토하자. 그 외에는 *기다리는 편이 낫다*. Valhalla가 들어오면 그때 다시 살펴봐도 늦지 않다.

## §18.3 Class-File API — ASM 시대의 종료

세 번째 질문. *ASM은 무엇으로 대체되는가?*

자바의 *부족 비밀* 같은 도구가 있다. **ASM**. OW2 컨소시엄의 바이트코드 조작 라이브러리. Spring AOP의 dynamic proxy가 ASM 위에서 돌고, Hibernate의 lazy proxy도 ASM. Lombok이 컴파일 타임에 바이트코드를 변형하고, ByteBuddy가 ASM을 감싸 더 친절한 API를 제공한다. CGLib, Javassist, BCEL — 모두 같은 자리에서 싸워 온 라이브러리들.

ASM은 강력하지만 *사용자 경험이 끔찍하다*. visitor 패턴, magic number 가득한 opcode 상수, 매 JDK 릴리스마다 새 class file format을 따라잡아야 하는 maintenance 부담. ASM 9.x에서 10.x로 가는 사이 깨진 코드가 한둘이 아니다. JDK가 새 instruction을 추가하면 ASM이 follow-up을 해야 하고, 그 사이 모든 ASM 의존 라이브러리가 같이 멈춘다.

### JEP 484 — 1급 API의 도입

| JEP | Java | 단계 |
|---|---|---|
| 457 | 22 | Class-File API (Preview) |
| 466 | 23 | Class-File API (Second Preview) |
| **484** | **24** | **Class-File API (Standard)** |

3년 만에 표준이 됐다. 모듈은 `java.lang.classfile` — `jdk.internal`이 아니라 *공식 java 네임스페이스 안*이다. 이 자리 자체가 의미한다. 바이트코드 조작이 더 이상 부족 비밀이 아니라 *언어 플랫폼의 일부*가 됐다는 선언.

기본 모양을 한 번 보자. "Hello"를 출력하는 클래스를 바이트코드로 생성하는 코드.

```java
import java.lang.classfile.*;
import java.lang.constant.*;
import static java.lang.constant.ConstantDescs.*;

byte[] bytes = ClassFile.of().build(
    ClassDesc.of("Hello"),
    cb -> cb.withFlags(ClassFile.ACC_PUBLIC)
        .withMethodBody("main",
            MethodTypeDesc.of(CD_void, CD_String.arrayType()),
            ClassFile.ACC_PUBLIC | ClassFile.ACC_STATIC,
            mb -> mb.getstatic(ClassDesc.of("java.lang.System"), "out",
                               ClassDesc.of("java.io.PrintStream"))
                    .ldc("Hello")
                    .invokevirtual(ClassDesc.of("java.io.PrintStream"), "println",
                                   MethodTypeDesc.of(CD_void, CD_String))
                    .return_())
);
```

ASM의 visitor 패턴이 *builder 패턴*으로 바뀌었다. `ClassFile.of().build(name, classBuilder -> ...)`가 시작점이고, 그 안에서 method를 추가하고, 그 안에서 instruction을 람다로 적는다. `ldc("Hello")`, `invokevirtual(...)`처럼 instruction이 *그 자체로 메서드 호출*이다. `ClassDesc`, `MethodTypeDesc`는 Java 12에서 들어온 `java.lang.constant` 패키지의 nominal descriptor — symbolic하게 클래스와 메서드를 가리키는 표준 표현.

ASM의 `ClassVisitor`, `MethodVisitor`, `visitMethodInsn(INVOKEVIRTUAL, ...)` 같은 모양과 비교가 되는가? *훨씬 자바스럽다*. 람다와 메서드 체이닝으로 자연스럽게 풀린다. *fluent*하다.

### 더 중요한 약속 — JDK와 함께 진화한다

API 모양보다 더 중요한 변화가 있다. *Class-File API는 JDK 안에 산다*. 새 instruction이 추가되면 같은 릴리스에서 API가 자동으로 따라온다. ASM이 6개월씩 지각하는 일이 없다. permits, sealed, record component, varhandle — JDK가 새 class file feature를 추가할 때 Class-File API는 *그 자리에서* 지원한다.

이 약속이 Spring AOT·Hibernate·Lombok 같은 라이브러리들에 던지는 신호는 크다. ASM 의존을 점진적으로 걷어낼 수 있다는 뜻이다. 새 JDK 릴리스마다 깨지는 일이 줄어든다는 뜻이다. *플랫폼 위에서* 바이트코드를 다룰 수 있다는 뜻이다.

### 예제 — ASM에서 Class-File API로

간단한 변환 예제. 모든 메서드에 진입 시 `System.out.println`을 끼워 넣는 instrumentation.

**ASM 시대 (개요만)**

```java
ClassReader reader = new ClassReader(originalBytes);
ClassWriter writer = new ClassWriter(reader, ClassWriter.COMPUTE_FRAMES);
ClassVisitor visitor = new ClassVisitor(Opcodes.ASM9, writer) {
    @Override
    public MethodVisitor visitMethod(int access, String name, String desc,
                                     String sig, String[] exc) {
        MethodVisitor mv = super.visitMethod(access, name, desc, sig, exc);
        return new MethodVisitor(Opcodes.ASM9, mv) {
            @Override
            public void visitCode() {
                mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
                mv.visitLdcInsn("entering " + name);
                mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println",
                                   "(Ljava/lang/String;)V", false);
                super.visitCode();
            }
        };
    }
};
reader.accept(visitor, 0);
byte[] result = writer.toByteArray();
```

`visit*` 메서드 다섯 개, internal name(`java/lang/System`), descriptor 문자열(`(Ljava/lang/String;)V`) — 모두 *낮은 층위*의 표현이다.

**Class-File API 시대**

```java
ClassFile cf = ClassFile.of();
ClassModel original = cf.parse(originalBytes);
byte[] result = cf.transform(original, ClassTransform.transformingMethodBodies(
    (codeBuilder, codeElement) -> {
        // 메서드 시작 시점에 println 삽입
        // (정확한 위치 분기는 첫 instruction 여부로 판단)
        codeBuilder.with(codeElement);
    }));
```

코드 분량이 줄어드는 건 부차적인 효과다. *진짜 차이*는 internal name이 아니라 `ClassDesc.of("java.lang.System")`을 쓴다는 것, descriptor 문자열이 아니라 `MethodTypeDesc`를 쓴다는 것이다. *자바의 정상 표현*으로 바이트코드를 다룬다.

Spring AOT가 받는 영향은 크다. Spring 6의 빌드 타임 BeanFactory 사전 계산은 결국 *바이트코드 생성*이다. Class-File API가 들어오면서 그 코드가 더 깔끔해지고, 새 JDK 릴리스마다 ASM upgrade에 발목 잡히는 일이 줄어든다. Hibernate의 lazy proxy 생성, Lombok의 컴파일 타임 변환 — 모두 같은 흐름이다. *11년 묵은 비밀이 표면으로 올라오고 있다*.

## §18.4 Project Panama의 야망 — 그리고 그 너머

세 절을 다 지나왔다. 한 번 멈춰 서서 *왜 이 셋이 한 장에 모였는지* 짚어보자.

**Project Panama**의 깃발 아래에 있다. Panama의 사명은 단순하다 — *자바와 native ecosystem 사이의 경계를 더 얇게 만들자*. JNI라는 두꺼운 벽을 얇은 막으로 바꾸자. FFM은 그 벽 자체를 허물었다. Vector API는 native CPU의 SIMD 명령을 *자바 코드로* 표현할 수 있게 했다. Class-File API는 JVM의 바이트코드를 *플랫폼의 일급 추상*으로 끌어올렸다. 셋 모두 "자바는 더 이상 native와 *분리된 섬*이 아니다"라는 같은 선언을 한다.

그 너머에는 무엇이 있는가? 22장에서 자세히 다루겠지만, 지도만 펼쳐 보자.

- **GPU 호출.** FFM + Vector API의 조합으로 CUDA·OpenCL·Metal을 자바에서 부르는 시도가 가능해진다. TornadoVM 같은 프로젝트가 그 길을 일찍 걷고 있다.
- **DPDK·io_uring.** 고성능 네트워킹 라이브러리를 자바가 직접 다룰 수 있다. JNI의 비용 없이.
- **ML inference.** ONNX Runtime, TensorRT 같은 ML 런타임을 자바에서 호출하면서, Vector API로 pre/post-processing을 같은 JVM에서 처리. *Java가 ML 추론 서버의 일급 후보가 된다*.
- **Cryptography.** libsodium·OpenSSL 같은 검증된 C 라이브러리를 직접. JCE provider의 무거운 추상 없이.

이 미래는 *이미 일부 도착해 있다*. Java 22 이상의 production 코드베이스에서 FFM은 정말로 JNI를 대체하고 있고, Vector API는 incubator임에도 ML 워크로드에서 진지하게 채택되고 있다. Class-File API는 Spring 7, Hibernate 7의 빌드 파이프라인을 새로 그리고 있다.

**Spring 맥락에서 정리하자.** FFM은 *암호화 라이브러리 호출*에서, Vector API는 *이미지 처리·ML 추론 마이크로서비스*에서, Class-File API는 *Spring AOT의 빌드 타임 코드 생성*에서 각자 자리를 잡는다. 셋 모두 *일반 비즈니스 로직*에는 직접 닿지 않는다. 그러나 *플랫폼 라이브러리*가 이 셋 위에서 다시 짜이면서, 그 위의 모든 Spring 앱이 *간접적으로* 영향을 받는다. JNI 의존 라이브러리가 FFM으로 갈아끼워지면 우리 컨테이너의 패키징이 단순해지고, Spring AOT가 Class-File API 위에서 빨라지면 우리 앱의 startup이 빨라진다. *우리가 직접 손대지 않아도, 발 아래의 흙이 바뀌고 있다*.

JNI `*.h` 추출에 하루를 쓰던 그날에서 11년이 흘렀다. 그 하루는 이제 5분이다. 이게 사실이라는 걸 우리가 받아들이는 데에는 시간이 좀 더 필요할지도 모른다. 그러나 *받아들이는 편이 낫다*. 다음 native 통합을 짤 때는 한 번 멈춰 서서, JNI 대신 FFM을 검토해보자. SIMD가 필요한 hot path를 만나면, JNI 우회 대신 Vector API를 살펴보자. 바이트코드 변환을 짜야 한다면, ASM 의존을 새로 들이기 전에 Class-File API를 먼저 펴 보자.

다음 장에서는 *시작 시간*의 영역으로 넘어간다. AOT, CDS, Leyden, Compact Object Headers — 자바가 GraalVM 없이도 빠른 startup을 손에 쥐는 새 풍경이다. 함께 가 보자.
