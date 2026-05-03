# 15장. JVM과 함께 — FFI·JNI·Project Panama·폴리글랏 아키텍처

이 책의 한 줄 결론을 먼저 박아두자. **Rust는 JVM의 대체가 아니라 무기 추가다.** 1장에서 약속한 한 줄이 15장에서 본격적으로 풀린다. 자네 회사의 Spring 시스템이 *훌륭하게 굴러가고 있는데*, 그 옆에 또는 그 안에 Rust를 어떻게 끼워 넣을 것인가? JNI가 있고, Project Panama가 있고, C ABI가 있고, gRPC 사이드카가 있다. 어느 다리를 어느 모양으로 놓아야 하는가? 그리고 그 다리 위에서 *UB(undefined behavior)*가 새지 않게 하려면 무엇을 잊지 말아야 하는가?

15장은 *떠나지 않는 도입*의 챕터다. *전부 Rust로 갈아엎자*는 단어는 어디에도 등장하지 않는다. 14장에서 만든 8MB 컨테이너를 *Spring 시스템의 짝꿍*으로 배치하는 길, 그리고 한 단계 더 들어가 *같은 프로세스 안에서 Rust 함수를 호출*하는 길까지 한 줄씩 풀어보자. 마지막에는 *AWS 비용 81% 절감* 사례를 솔직한 한 단락으로 회상하자. 이 챕터의 마지막에서도 한 번 더 박을 것이다 — Rust는 JVM의 대체가 아니라 무기 추가다.

## 폴리글랏 전략의 정석 — 세 가지 패턴

JVM 시스템에 Rust를 들이는 길은 사실상 세 가지다. *거리·격리·지연·복잡도*의 4축으로 trade-off가 갈린다. 표 한 줄로 먼저 정리해두자.

| 패턴 | 거리 | 프로세스 격리 | 호출 지연 | 도입 복잡도 | 어울리는 자리 |
|---|---|---|---|---|---|
| **사이드카(gRPC/HTTP)** | 같은 노드/파드 | 강함 | µs~ms 단위 | 낮음 | 이미지 처리, 검색, 변환 |
| **hot path 추출(별도 서비스)** | 같은 클러스터 | 강함 | ms 단위 | 중간 | 매칭 엔진, 인증, 게이트웨이 |
| **in-process FFI(JNI/Panama)** | 같은 프로세스 | 없음 | ns~µs 단위 | 높음 | 해시·인코딩·압축 같은 순수 함수 |

세 패턴은 *어느 하나만 골라야 하는* 양자택일이 아니다. 회사 시스템 전체에서 *위치별로 다르게* 고를 수 있다. 한 줄씩 풀어보자.

### 사이드카 패턴 — 가장 부담이 적은 출발점

14장에서 만든 8MB 컨테이너를 Spring 시스템 옆에 *그냥 한 파드 안의 사이드카*로 배치한다. Spring 측에서는 `localhost:8081`로 gRPC나 HTTP를 한 번 부르면 된다. *프로세스가 분리되어 있어* Rust 측에서 panic이 나도 JVM 측은 영향을 받지 않는다. 가장 안전한 출발점이다.

```yaml
# kubernetes deployment.yaml — 일부
spec:
  containers:
  - name: spring-app
    image: registry/myapp:1.0
  - name: rust-sidecar
    image: registry/myapp-rust:1.0   # 8MB 이미지
    ports:
    - containerPort: 8081
```

Spring 측 호출은 익숙한 모양이다.

```java
@RestController
class ImageController {
    private final WebClient client = WebClient.create("http://localhost:8081");

    @PostMapping("/thumbnail")
    public Mono<byte[]> thumbnail(@RequestBody byte[] image) {
        return client.post().uri("/resize")
            .bodyValue(image)
            .retrieve().bodyToMono(byte[].class);
    }
}
```

WebClient 한 줄로 끝난다. 처음 도입할 때는 *내부 도구*나 *비크리티컬 hot path* 한두 개부터 시작하는 편이 낫다. 운영팀이 *이게 뭐였지*에 빠지지 않게, *왜 이 사이드카가 거기 있는지*를 한 페이지짜리 RFC로 남겨두자. 16장에서 다시 짚을 *조직 도입의 정치*에서 가장 효과가 큰 한 줄이다.

### hot path 추출 — 별도 서비스로 떼어내기

조금 더 진지한 자리는 hot path 추출이다. 사이드카처럼 *한 파드 안에* 있을 필요가 없는, *별도 서비스로 분리*한 모양이다. 이미지 처리 파이프라인, 매칭 엔진, 데이터 직렬화 모듈, 인증 체크 — 자네 시스템에서 *CPU·메모리를 가장 많이 먹는 한 자리*가 후보다. 그 한 자리만 Rust로 옮겨도, 14장에서 본 *20~30배 메모리 절감*과 *5~10배 처리량 증가*가 그대로 따라온다.

이쯤에서 한 사례를 짚어보자. *"I Replaced My Spring Boot Microservice with Rust and Go"*라는 후기 글이 있다. 단일 hot path만 분리해 *AWS 비용을 81% 줄였다*는 보고다. 핵심은 *전체를 옮기지 않았다*는 점이다. 비즈니스 로직 다수는 Spring/Kotlin 그대로 두고, *변환 + 캐싱이 무거웠던 한 자리*만 떼어냈다. 그 후 *기술적으로도 정치적으로도 성공*했다는 한 줄로 글이 닫힌다. *기술 성공·정치 성공*의 두 박수가 동시에 들어와야 한다는 점은 16장에서 다시 짚자.

Cloudflare의 Pingora도 같은 결의 사례다. Nginx + Lua 기반 reverse proxy의 *hot path 한 자리*를 Rust로 다시 짜서 *CPU 70% 절감, 메모리 67% 절감*을 얻었다. 일일 1조 건이 넘는 요청을 처리하면서다. Discord의 Read States 서비스도 *Go GC의 2분마다 spike*를 *Rust 단일 컴포넌트로 분리*해 풀었다. 패턴은 같다. *전체*가 아니라 *한 자리*다.

### in-process FFI — 같은 프로세스 안에서 호출

마지막은 가장 가까운 거리다. JVM 프로세스 안에서 *Rust 함수를 직접 호출*한다. JNI 또는 Project Panama가 그 길이다. 호출 지연은 *나노초 단위*로 떨어지지만, *프로세스 격리가 없다*. Rust 측에서 panic이 새면 JVM이 *Segmentation Fault*로 죽는다. 가장 강력하지만 가장 위험한 길이다. 그래서 이 길은 *순수한 계산*에 집중한다. SHA-256 해시, ZSTD 압축, base64 인코딩, 정규식 매칭 — *외부 자원에 손대지 않는* 함수일수록 안전하다.

세 패턴 중 어느 것이 자네 자리에 맞을까? *모르겠으면 사이드카부터*. 사이드카로 운영해본 경험이 쌓이면 *프로세스 분리의 비용*이 얼마인지 손에 묻혀진다. 그 비용이 정말 아쉬워질 때, 한 단계 안으로 들어가 in-process FFI를 시도해보면 된다. 처음부터 in-process로 들어가는 것은 *난이도가 높다*. 잊지 말자.

## JNI로 JVM에서 Rust 호출

JNI 자체는 자바 출신에게 절반은 익숙한 길이다. *Java 측 코드*를 짜본 적이 있다면, 이 절은 *그 익숙함의 반대편(Rust 측)*을 이어주는 다리다. `jni` crate를 쓰자.

먼저 Java 측 선언이다. *native 메서드*를 한 줄 적어두면 된다.

```java
// io/example/HashLib.java
public final class HashLib {
    static { System.loadLibrary("hashlib"); }
    public static native String sha256Base64(String input);
}
```

이제 Rust 측이다. `Cargo.toml`에 한 단락을 박는다.

```toml
[lib]
name = "hashlib"
crate-type = ["cdylib"]

[dependencies]
jni = "0.21"
sha2 = "0.10"
base64 = "0.22"
```

본 코드는 이렇게 적는다. JNI 함수의 이름 규약은 *Java\_패키지\_클래스\_메서드*다.

```rust
use base64::{engine::general_purpose::STANDARD, Engine as _};
use jni::objects::{JClass, JString};
use jni::sys::jstring;
use jni::JNIEnv;
use sha2::{Digest, Sha256};

#[no_mangle]
pub extern "system" fn Java_io_example_HashLib_sha256Base64<'a>(
    mut env: JNIEnv<'a>,
    _class: JClass<'a>,
    input: JString<'a>,
) -> jstring {
    // JString → Rust String (소유권 가져오기)
    let input_owned: String = match env.get_string(&input) {
        Ok(s) => s.into(),
        Err(_) => return std::ptr::null_mut(),
    };

    // 진짜 일은 safe Rust로 — UB 회피의 첫 번째 원칙
    let digest = Sha256::digest(input_owned.as_bytes());
    let encoded = STANDARD.encode(digest);

    // Rust String → JString
    env.new_string(encoded)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}
```

`#[no_mangle]`은 *함수 이름을 mangling 없이 그대로* 쓰라는 표시다. JNI 측에서 정확한 이름으로 찾아야 하니 필수다. `extern "system"`은 OS가 정한 ABI(Linux x86_64에서는 System V AMD64)를 쓰라는 선언이다.

8장에서 *unsafe 한 절*을 봤던 기억이 있는가? 그때 약속한 회수가 여기다. *왜 JNI 함수가 사실상 unsafe인가?* 두 가지 이유다. 첫째, *JVM이 넘겨주는 jstring/jobject가 진짜로 살아있는 객체인지*를 Rust 측이 보장할 수 없다. JVM의 GC가 *호출 도중*에 그 객체를 옮겨버릴 수도 있다(`JNIEnv`의 local frame이 그래서 존재한다). 둘째, *Rust 측에서 panic이 나면* 그 panic이 JVM 측으로 *unwinding*되며 프로세스 전체가 *죽는다*. 그래서 *JNI 함수의 본문*은 *한 줄도 panic이 나지 않게* 정성껏 다뤄야 한다.

처방은 정해져 있다. *JNI 함수 본문은 외피로만 쓰고, 진짜 일은 safe Rust 함수에 위임*한다. 위 코드도 그 패턴이다. `JString` → `String` 변환만 외피에서 하고, SHA-256 해시는 평범한 safe 함수가 끝낸다. 이 한 줄짜리 규율이 UB의 90%를 막는다. 잊지 말자.

빌드는 `cargo build --release`로 끝난다. macOS에서는 `target/release/libhashlib.dylib`, Linux에서는 `target/release/libhashlib.so`가 떨어진다. JVM 측 `-Djava.library.path`에 그 디렉터리를 박으면 끝이다.

### `catch_unwind`로 panic 막기

이름 그대로 panic이 FFI 경계를 넘는 것을 *잡는* 함수다. `std::panic::catch_unwind`로 본 함수를 감싸 두면, panic이 났을 때 Rust 측에서 *Java 예외*로 변환해 다시 던질 수 있다.

```rust
#[no_mangle]
pub extern "system" fn Java_io_example_HashLib_sha256Base64<'a>(
    mut env: JNIEnv<'a>,
    _class: JClass<'a>,
    input: JString<'a>,
) -> jstring {
    let result = std::panic::catch_unwind(|| {
        // ... 위 본문과 동일
        let s: String = env.get_string(&input).ok()?.into();
        Some(STANDARD.encode(Sha256::digest(s.as_bytes())))
    });

    match result {
        Ok(Some(s)) => env.new_string(s).map(|j| j.into_raw())
                          .unwrap_or(std::ptr::null_mut()),
        Ok(None) => std::ptr::null_mut(),
        Err(_) => {
            // Java RuntimeException으로 던지기
            let _ = env.throw_new("java/lang/RuntimeException", "Rust 측 panic");
            std::ptr::null_mut()
        }
    }
}
```

이 한 단락이 *FFI 경계의 안전벨트*다. `panic = "abort"` 빌드(14장의 release 프로파일 튜닝에서 본)와 함께 쓰면 *panic이 일어나는 즉시 프로세스가 죽는 모양*이 되어, 오히려 디버깅이 쉬워질 때도 있다. 어느 쪽을 고를지는 자네 자리의 신뢰성 요구에 달렸다.

## C ABI와 `#[repr(C)]` — 데이터 경계의 모양

JNI 외에도 *C ABI*를 직접 노출하는 길이 있다. JNR-FFI나 Project Panama처럼 *C ABI를 통해 Rust dylib을 호출*하는 자리에서 필요하다. 핵심은 *Rust struct의 메모리 layout*을 C 호환으로 강제하는 일이다.

기본 Rust struct는 *컴파일러가 마음대로 필드를 재배치*한다. 패킹·정렬·ABI에 대한 가정을 다른 언어 측이 *다르게* 하면 *조용히* 데이터가 깨진다. 가장 흔한 사고다. 처방은 attribute 한 줄이다.

```rust
#[repr(C)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

#[repr(C)]
pub enum Color {
    Red,
    Green,
    Blue,
}

#[no_mangle]
pub extern "C" fn distance(a: Point, b: Point) -> f64 {
    ((a.x - b.x).powi(2) + (a.y - b.y).powi(2)).sqrt()
}
```

`#[repr(C)]`는 *C 컴파일러가 같은 struct를 짤 때와 같은 레이아웃*을 강제한다. `#[repr(transparent)]`는 *단일 필드 newtype*에 쓴다 — wrapper를 끼워도 ABI 상으로는 *내부 타입과 동일*하다는 약속이다. `#[repr(u8)]`은 enum의 *discriminant 크기*를 명시한다. JVM Panama나 JNR-FFI 측에서 *struct layout을 어떻게 가정할지*가 이 한 줄로 정해진다.

C 헤더 파일을 손으로 적기는 *번거롭다*. `cbindgen`이라는 도구가 그 일을 자동으로 한다.

```bash
cargo install cbindgen
cbindgen --crate mycrate --output include/mycrate.h
```

```c
// include/mycrate.h — 자동 생성
typedef struct Point {
  double x;
  double y;
} Point;

double distance(Point a, Point b);
```

자바 Panama의 `jextract`도 같은 발상이다. *언어 사이의 헤더는 사람이 손으로 적는 것이 아니라 도구가 만든다*는 원칙을 마음에 박자. 손으로 적은 헤더는 *조용히 어긋나는 사고*의 가장 흔한 원인이다.

## Project Panama — 가장 깔끔한 미래

JEP 442/454로 GA가 된 Project Panama는 JVM의 차세대 native interop이다. `Foreign Function & Memory API(FFM API)`로 *JNI 보일러플레이트 없이* Rust dylib을 호출할 수 있다. Java 22+가 기본이다.

```java
// Project Panama 스타일
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;

public final class HashLib {
    private static final SymbolLookup LIB =
        SymbolLookup.libraryLookup("hashlib", Arena.global());
    private static final MethodHandle SHA = Linker.nativeLinker().downcallHandle(
        LIB.find("sha256_hex").orElseThrow(),
        FunctionDescriptor.of(
            ValueLayout.ADDRESS,   // 반환: 문자열 포인터
            ValueLayout.ADDRESS    // 인자: 입력 문자열 포인터
        )
    );

    public static String sha256Hex(String input) throws Throwable {
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment in = arena.allocateUtf8String(input);
            MemorySegment out = (MemorySegment) SHA.invokeExact(in);
            return out.reinterpret(64).getUtf8String(0);
        }
    }
}
```

이 모양의 매력은 두 가지다. 첫째, *jextract 도구로 헤더에서 자동 바인딩이 생성*된다. 위 코드도 사람이 직접 적기보다는 *도구가 만든 모양*에 가깝다. 둘째, *Arena로 메모리 수명*을 명시적으로 관리한다 — JNI의 local frame보다 *훨씬 솔직한 모델*이다. JVM 출신이 *익숙한 try-with-resources* 모양 그대로다.

*현재 가장 깔끔한 미래*라는 평이 흔하다. 단, JNI vs Panama의 *latency/throughput 정량 비교* 자료는 본 책의 리서치 시점에서 충분히 모이지 않았다(reference 8 한계 2). JEP 442/454의 GA 이후 측정 데이터가 더 모이면 *어느 쪽이 얼마나 빠른지*가 명확해질 것이다. 지금 시점에서는 *새로 시작하는 폴리글랏*이라면 Panama를, *기존 JNI 코드와 호환을 유지해야 한다*면 JNI를 권한다.

JNR-FFI는 또 다른 대안이다. C ABI 기반이라 *Rust 측에 JNI 의존성이 없다*는 매력이 있다. JNI보다 가볍지만 Panama 등장으로 *위치가 애매해지는 중*이다. 새 프로젝트라면 Panama를 먼저 고려하는 편이 낫다.

## UB 회피의 표준 패턴 — 다섯 가지 체크리스트

FFI는 *unsafe의 가장 큰 사용처*다. 한 줄 실수가 *segfault → 데이터 손상 → 보안 사고*로 빠르게 미끄러질 수 있다. 8장 unsafe 절에서 짚었던 원칙을 *FFI 자리*에 맞게 다시 적어두자. 다섯 줄로 외워두면 좋다.

**1. unsafe API는 항상 safe wrapper 뒤에 둔다.**

```rust
// 나쁜 예 — 호출하는 사람이 매번 unsafe 책임을 짐
pub unsafe fn read_buffer(ptr: *const u8, len: usize) -> Vec<u8> {
    std::slice::from_raw_parts(ptr, len).to_vec()
}

// 좋은 예 — 호출자는 safe 함수만 본다
pub fn read_buffer(ptr: *const u8, len: usize) -> Option<Vec<u8>> {
    if ptr.is_null() || len == 0 { return None; }
    // 안전 조건이 위에서 검증됐으니 여기서만 unsafe
    let slice = unsafe { std::slice::from_raw_parts(ptr, len) };
    Some(slice.to_vec())
}
```

unsafe 블록이 *어디서 시작해서 어디서 끝나는지*가 한 줄로 보이는 모양이다. 호출자는 *safe 함수만 보고도 안심*할 수 있다.

**2. lifetime이 불분명한 raw pointer는 즉시 owned로 복사한다.**

JNI/Panama에서 받은 포인터가 *언제까지 유효한지*는 보통 *한 번의 호출 동안*만 보장된다. Rust 측에서 그 포인터를 *struct 안에 보관*하는 순간 사고다. 들어오자마자 `.to_vec()`이나 `.to_owned()`으로 *복사*하자. 비용이 한 번 더 들지만 *마음의 평화*는 그 이상이다.

**3. JVM 측 Java 객체는 JNIEnv local frame을 명시적으로 관리한다.**

긴 루프에서 Java 객체를 반복 생성하면 *local reference table이 차서* JVM이 죽는다. `env.with_local_frame(16, |env| { ... })`로 *프레임 범위*를 명시적으로 잡자. JNI 책에서 가장 자주 등장하는 사고다.

**4. panic은 절대 FFI 경계를 넘지 않게 한다.**

위에서 본 `catch_unwind`다. *외피 함수에 한 번만* 깔아두면 된다. `panic = "abort"` 프로파일과 조합해 *방어선을 두 겹*으로 두는 팀도 많다.

**5. `cargo miri`로 unsafe 코드를 검증한다.**

miri는 *Mid-level IR Interpreter*다. Rust 코드를 *AST 직전 단계에서 해석*하면서 *UB가 발생하는 순간*을 잡아낸다. 일반 테스트로는 잡히지 않는 *aliasing 위반*이나 *uninitialized 메모리 접근*이 한 줄로 드러난다.

```bash
rustup +nightly component add miri
cargo +nightly miri test
```

CI에 miri를 게이트로 박아두는 팀도 있다. 빌드 시간이 *몇 배*로 늘어 매 PR에는 어렵지만, *주 1회 정기 실행*은 충분히 현실적이다. unsafe 코드의 안전망을 한 단계 더 두는 셈이다.

학술 인용을 한 줄 보태두자. *deepSURF*라는 도구가 IEEE S&P 2026에 발표됐다. *FFI 경계의 메모리 안전성을 자동으로 검증*하는 정적 분석기다. 산업 도구로 내려오기까지는 시간이 더 걸리겠지만, *학계가 같은 문제를 같은 자리에서 풀고 있다*는 신호로 알아두자. FFI 안전성은 우리만 고민하는 문제가 아니다.

## 사이드카가 아닌 또 다른 모양들

세 패턴(사이드카·hot path·FFI) 외에도 알아두면 좋은 변형이 두 가지 있다. *결*을 풍성하게 만들어주는 자리들이다.

### Mozilla application-services 패턴

한 Rust crate를 iOS·Android·Desktop이 *공유*하는 모양이다. Mozilla의 [application-services](https://github.com/mozilla/application-services) 저장소가 가장 잘 정돈된 사례다. 인증, 로그인, 동기화 같은 *비즈니스 로직 코어*를 Rust로 짜고, 각 플랫폼은 *JNI(Android), Swift(iOS), Electron 바인딩(Desktop)*로 호출한다. *코드 중복이 사라지는 동시에* 메모리 안전성이 따라온다. 백엔드 책의 스코프 밖이지만, *Kotlin Multiplatform과 같은 발상*이라는 한 줄을 알아두자. Rust가 *모바일까지 한 손에 잡는* 자리에 닿는다.

### WebAssembly — 또 다른 배포 단위

Wasmtime, Wasmer, Spin, wasmCloud 같은 런타임이 *사이드카가 아닌 또 다른 배포 단위*로 떠오르는 중이다. Rust 코드를 `wasm32-wasi` 타겟으로 컴파일하면 *어떤 호스트에서도 동일하게 도는* 작은 모듈이 된다. JVM의 *컴파일 한 번 어디서나 실행*이라는 약속을 *런타임 없이* 풀어내는 모양이다. 백엔드 책의 본 스코프는 아니지만, *플랫폼 간 이식성*이 화두인 자리에서 자주 등장한다. 한국 사례로는 일부 핀테크가 *내부 룰 엔진*을 wasm으로 풀고 있다는 신호도 들린다. 알아두자.

### no_std·임베디드 한 단락

마지막으로 *백엔드 출신이 가장 만나기 어려운* 영역 한 줄을 짚어두자. `no_std`는 *표준 라이브러리 없이 컴파일되는 Rust*다. heap allocation 자체를 *선택적*으로 한다. 임베디드, 펌웨어, 커널 모듈, 부트로더 — Rust는 이 영역에서도 *운영체제 없는 자리*를 메우고 있다. arXiv의 *"Rust for Embedded Systems: Current State and Open Problems"*가 잘 정리해둔 한 편이다.

백엔드 자네에게는 *직접 만질 자리는 거의 없다*. 다만 회사가 IoT·하드웨어·드론 같은 자리로 확장될 때 *Rust가 그 자리에서도 같은 언어로 통한다*는 사실이 *전략적 자산*이 된다. 한 표 더 적어두자.

| 영역 | Rust 자리 | JVM 자리 |
|---|---|---|
| 백엔드 서비스 | 가능(이 책의 본 스코프) | 가능(주력) |
| 모바일 | 가능(application-services 패턴) | Android 가능, iOS 어려움 |
| 데스크톱 | 가능(Tauri, egui) | 가능(JavaFX) |
| 임베디드 | 가능(no_std) | 어려움(GraalVM도 한계) |
| 커널·드라이버 | 가능(Linux/Windows kernel 채택 중) | 거의 없음 |
| WebAssembly | 1급 시민 | 일부 가능(TeaVM) |

JVM이 비워두는 칸이 보일 것이다. *그 빈칸*이 Rust의 자리다. 이 자리들을 잠재적으로 *손에 쥘 수 있다*는 사실이, 자네 회사의 5년 후 기술 지도에 *한 줄짜리 보험*이 된다. 무기 추가다.

## 솔직한 사례 회상 — AWS 비용 81% 절감

15장을 닫으면서 한 사례를 솔직하게 회상하자. *"I Replaced My Spring Boot Microservice with Rust and Go"* 글의 한 단락이다.

저자는 처음부터 *Rust로 다 옮기겠다*고 결심하지 않았다. 자기 시스템의 *AWS 청구서*를 보다가, *변환 + 캐싱이 무거웠던 한 자리*가 비용의 절반을 차지한다는 사실을 발견했다. *그 한 자리만* 떼어 Rust로 다시 짰다. 결과는 *AWS 비용 81% 절감*이었다. 비즈니스 로직 다수는 Spring/Kotlin 그대로 두었다. *기술적으로도 정치적으로도 성공*했다는 한 줄로 글이 닫힌다.

이 사례에서 마음에 새겨야 할 한 줄은 *전체*가 아니라 *한 자리*라는 점이다. *전부 Rust로 갈아엎자*는 결심은 *대부분의 자리에서 정치적 실패*로 끝난다(다음 16장에서 그 그늘을 솔직하게 보자). 반대로 *가장 무거운 한 자리*를 골라 *조용히 다리를 놓는* 결심은 *기술과 정치 두 박수*를 동시에 받는다.

Cloudflare의 Pingora도 같은 모양이다. Nginx 전체를 갈아엎지 않고, *reverse proxy 한 자리*만 다시 짰다. Discord의 Read States도, AWS의 Firecracker도 마찬가지다. *한 자리*다. 자네 회사 시스템에서 *그 한 자리*가 어디인지 — 답은 자네의 모니터링 대시보드 어딘가에 이미 적혀 있다.

## 다시 한 줄로 — Rust는 JVM의 대체가 아니라 무기 추가다

이 챕터의 처음과 같은 한 줄로 닫자. **Rust는 JVM의 대체가 아니라 무기 추가다.** 8MB 사이드카는 그 무기의 한 모양이고, JNI/Panama로 호출되는 순수 함수는 또 다른 모양이다. 어느 모양을 골라도 *JVM을 떠나지 않는다*. *떠나지 않으면서 더 잘하게 된다*는 약속이 이 챕터 전체를 관통한다.

자네 회사의 시스템 지도를 펴보자. 비즈니스 로직 다수는 Spring/Kotlin 그대로 두자. CPU·메모리 가장 많이 먹는 *한 자리*를 골라 사이드카로 떼어 보자. *그 한 자리에서 시작된 변화*가 어디까지 갈지는 — 이 책 다음의 자네 손에 달려 있다. 그것이 16장의 본 주제다.

## 마무리 — 함께 해보자

13장 워크스페이스의 도메인 crate에서 *순수 함수 하나*를 골라보자. SHA-256 해시 + Base64 인코딩 같은, *외부 자원에 손대지 않는* 깔끔한 함수가 좋다. 그 함수를 JNI로 노출해보자. Spring Boot 측에 작은 컨트롤러를 만들어 호출해보고, JFR로 measure해 *같은 함수를 Java로 짠 것*과 처리량을 비교하자. 그다음 같은 함수를 Project Panama 바인딩으로도 노출해 *JNI vs Panama의 보일러플레이트 양 차이*를 손으로 확인해 보자. 두 모양이 같은 일을 *얼마나 다른 모양으로* 해내는지 한 단락으로 정리해두면 좋다. 마지막으로 그 hot path를 *별도 사이드카 컨테이너*로 한 번 떼어내 보자. *세 가지 패턴*을 한 함수로 다 해본 셈이 된다. *(이 hot path 분리 경험은 16장의 *조직 도입 전략*에서 다시 호출된다.)*

여기서부터는 책 안의 다음 챕터가 아니라 *부록 A의 JVM↔Rust 매핑 표를 자네 책상에 펴두고*, 자기 시스템에서 *어디부터 Rust로 옮길지*를 한 줄씩 적어보자. 본문에 산발적으로 박힌 매핑이 *한 페이지에 모인 모양*이라 hot path 후보 결정이 한층 빨라진다. 그 한 줄들이 다음 16장의 *조직 도입 전략*과 그대로 이어진다.

다음 16장에서는 사람과 조직의 자리로 간다. 4~6개월의 학습 곡선, 도입의 정치, 한국 커뮤니티 자원, 그리고 책의 마지막 매듭이 기다리고 있다.

## 참고

- 폴리글랏 전략(사이드카·hot path·FFI) — reference 토픽 12, 토픽 10.3
- JNI(`jni-rs`) 사용법 — reference 토픽 10.3, jni-rs docs
- Project Panama(JEP 442/454) — reference 토픽 10.3
- C ABI / `#[repr(C)]` / cbindgen — reference 토픽 2 보강, 토픽 10.3
- UB 회피 패턴 — reference 토픽 4·8 보강, deepSURF (IEEE S&P 2026)
- Mozilla application-services — reference 토픽 10.3
- AWS 비용 81% 절감 사례 — reference 4.8
- Cloudflare Pingora, Discord Read States — reference 4.1·4.2
