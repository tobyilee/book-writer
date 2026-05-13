# 5장 — overflow라는 무덤

> "ADC 한 줄이 왜 틀렸는지 3일 동안 못 찾았다."
> 레트로 컴퓨팅 커뮤니티의 흔한 고백이다.

## 핵심 질문

8비트 덧셈은 왜 입문자의 90%가 걸려 넘어지는가?  
그리고 **테스트 한 방**으로 어떻게 그 함정을 전부 잡는가?

## 이 장에서 배우는 것

### 4개 플래그의 정체

| 플래그 | 이름 | 언제 1이 되는가 |
|--------|------|----------------|
| **Z** | Zero | 결과가 0x00 |
| **C** | Carry | 8비트를 초과하는 올림수 발생 (덧셈) / 빌림수 없음 (뺄셈) |
| **S** | Sign | 결과의 비트 7 = 1 (음수처럼 해석) |
| **V** | Overflow | 부호 있는 8비트 범위 −128 ~ 127 초과 |

Z와 C는 직관적이다. S도 비트 마스킹이면 끝이다.  
**V(overflow)**가 무덤이다.

### V 플래그의 수학

Ken Shirriff의 분석을 따르면:

```
V = (양수 + 양수 = 음수)  또는  (음수 + 음수 = 양수)
```

구현으로 옮기면:

```kotlin
val signedA = a.toByte().toInt()   // 0x80 → -128
val signedB = b.toByte().toInt()
val signedSum = signedA + signedB
overflow = signedSum < -128 || signedSum > 127
```

`toByte().toInt()`이 핵심이다. `0x80`을 `Int`로 그냥 쓰면 128이지만  
`toByte()`를 거치면 −128이 된다. 이 한 줄이 부호 있는 해석을 가능하게 한다.

## AluFlags — 설계 결정

`Alu` (chapter-04) 는 `Int` 하나를 돌려줬다.  
`AluFlags` 는 `AluResult` data class를 돌려준다.

```kotlin
data class AluResult(
    val value: Int,
    val zero: Boolean,
    val carry: Boolean,
    val sign: Boolean,
    val overflow: Boolean,
)
```

`data class`는 `copy()` + `==` + `toString()`을 공짜로 준다.  
테스트에서 `shouldBe`가 필드 단위로 비교할 수 있는 이유가 여기 있다.

## 이 장의 테스트 전략

### 왜 65,536 케이스인가

256 × 256 = 65,536.  
모든 8비트 피연산자 쌍을 전수 검증한다. 실행 시간은 JVM 기준 < 200 ms.  
경계값 몇 개를 고르는 것보다 수학적으로 완전하다.

```kotlin
for (a in 0..255) for (b in 0..255) {
    val signedSum = a.toByte().toInt() + b.toByte().toInt()
    AluFlags.add(a, b).overflow shouldBe (signedSum < -128 || signedSum > 127)
}
```

add와 sub 각각 5개/3개 속성 검증 → **131,072 개별 단언(assertion)**.

### 파일 구조

| 파일 | 역할 |
|------|------|
| `AluFlagsTest.kt` | 구체적인 대표 케이스 — 왜 그 숫자인지 주석으로 설명 |
| `AluFlagsOverflowSpec.kt` | 256×256 전수 검증 — 수학과 구현의 일치를 증명 |

두 계층을 유지하는 이유: 전수 검증은 **존재**를 보증하고,  
구체 케이스는 **의도**를 문서화한다.

## 실행

```bash
./gradlew :chapter-05:test
```

예상 출력 (Kotest DescribeSpec):

```
AluFlagsTest > AluFlags.add 기본 케이스 > 0 + 0 PASSED
AluFlagsTest > AluFlags.add 기본 케이스 > 100 + 50 PASSED
AluFlagsTest > AluFlags.add 기본 케이스 > 255 + 1 (carry) PASSED
AluFlagsTest > AluFlags.add 기본 케이스 > Sign 플래그 (음수 결과) PASSED
AluFlagsTest > AluFlags.sub 기본 > 10 - 5 PASSED
AluFlagsTest > AluFlags.sub 기본 > 5 - 10 (borrow) PASSED
AluFlagsOverflowSpec > AluFlags.add — 모든 256×256 = 65,536 조합 > 결과는 (a+b) mod 256 PASSED
...
```

총 **24개 테스트**, 131,072 단언 포함.

## 다음 장으로

플래그를 만들었다. 이제 플래그를 **읽는** 것이 문제다.  
6장은 상태 레지스터 (SR / P 레지스터) 를 도입한다 —  
8개 비트에 Z·C·S·V·I·D·B를 패킹하고, 언패킹하고, 분기 조건에 연결하는 과정을.

---

> 참고: Ken Shirriff, ["The 6502 overflow flag explained mathematically"](https://www.righto.com/2012/12/the-6502-overflow-flag-explained.html), 2012.
