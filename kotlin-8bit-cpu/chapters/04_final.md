<!-- 개정: 2026-05-13 style-guardian 라운드 1 반영 — Should 1~6, Nice 7·8 -->

# 4장. 레지스터와 8비트 산술 — 비트로 다시 익히는 덧셈

학부 1학년 시절의 코드 한 줄을 떠올려보자. 그때 우리는 처음으로 `byte`라는 타입을 만나고, 두 수의 합이 음수로 떨어지는 광경을 보고 머리를 긁었다. `byte a = 100; byte b = 50; byte c = (byte)(a + b);` — 그리고 `c`는 -106이 된다. 무슨 일이 일어난 건가? 100과 50을 더해서 음수가 나오다니, 컴퓨터가 고장난 게 아닌가?

물론 컴퓨터는 고장난 게 아니었다. 우리가 "8비트로 수를 표현한다"는 사실의 정확한 의미를 몰랐던 것이다. signed byte는 -128부터 127까지밖에 못 담는다. 150은 그 범위를 넘어선다. 비트는 그 자리에서 그대로 살아 있지만, 그것을 부호 있는 수로 해석하는 순간 의미가 뒤집힌다. 그것을 그제야 알았다. 그러고는 두 번 다시 떠올리지 않았다. JVM은 우리에게 `Int`라는 32비트의 넓은 우주를 줬고, 평범한 비즈니스 로직에서 byte를 직접 만질 일은 거의 없었기 때문이다.

그런데 SAP-1을 짓기 시작한 이상, 우리는 그 좁은 우주로 돌아가야 한다. SAP-1의 A 레지스터는 정확히 8비트다. ALU도 8비트 입력 두 개를 받아 8비트 출력 하나를 내놓는다. 그 위에서 덧셈을 하고 뺄셈을 하고 논리 연산을 한다. 학부 1학년의 그 멍한 표정으로 돌아가서는 곤란하다. 8비트 산술을 손에 잡힐 만큼 익혀두는 편이 낫다. 그래야 다음 장의 overflow 플래그 같은, **90%의 입문자가 막히는 지점**을 우리 손으로 통과할 수 있다.

네 가지를 함께 짚어보자. 첫째, 레지스터를 Kotlin 클래스로 어떻게 모델링할 것인가. 둘째, 2의 보수가 정확히 무슨 일을 하는가. 셋째, 가산기·감산기·논리 연산을 어떻게 짜고 어떻게 테스트할 것인가. 그리고 넷째 — 이게 가장 무거운 결정이다 — **이 책 전체에서 8비트 값을 `Int`로 다룰지 `UByte`로 다룰지의 정책**. 그 결정을 4장에서 정면으로 내려보자. 자, 시작해보자.

## 4.1 레지스터 — 작은 책장 하나

레지스터란 무엇일까? 한 줄로 답하면, **CPU 안에 들어 있는 작은 책장**이다. 한 칸에 8비트(또는 16비트, 32비트)짜리 값 하나가 들어간다. 메모리에 비하면 칸 수는 극도로 적지만, 접근 속도가 압도적으로 빠르다. CPU가 한 박자에 한 번씩 자기 책장에서 값을 꺼내거나 새 값을 적는다.

SAP-1의 레지스터는 매우 단출하다. A(누산기), B(가산기 입력), MAR(메모리 주소), IR(명령어), OUT(출력). 다섯 칸이 전부다. 각 칸은 8비트짜리 값을 담는다(MAR과 IR의 일부는 4비트지만 일단 잊자). 이 다섯 칸 안에서 컴퓨터의 모든 상태가 매 순간 흐른다.

이걸 Kotlin 코드로 옮기는 길은 두 가지다. 하나는 그저 `var` 속성으로 쓰는 길.

```kotlin
class Sap1 {
    var a: Int = 0
    var b: Int = 0
    var mar: Int = 0
    // ...
}
```

빠르고 단순하다. 단점은 "이 값은 8비트 범위를 넘으면 안 된다"는 약속을 코드가 명시적으로 지키지 않는다는 점이다. 누가 실수로 `a = 300`이라고 적어도 컴파일러가 막아주지 않는다. 다른 길은 작은 클래스로 감싸는 길이다.

```kotlin
class Register8(initial: Int = 0) {
    var value: Int = initial and 0xFF
        set(newValue) {
            field = newValue and 0xFF
        }

    override fun toString(): String =
        "0x${value.toString(16).padStart(2, '0').uppercase()}"
}

class Sap1 {
    val a = Register8()
    val b = Register8()
    val mar = Register8()
}
```

setter에서 `and 0xFF`를 강제하니까 누가 무엇을 넣어도 0~255 사이의 값으로 자르고 들어간다. 디버깅 시 `toString()`을 호출하면 `0x4F` 같은 16진수 표현이 나온다. 약간의 보호막이 생기고, 디버깅이 편해진다.

어느 쪽이 더 나을까? 한 줄로 답하기 어렵다. ksim65 같은 성숙한 시뮬레이터는 `var Int` 패턴으로 간다 — 가장 단순하고 가장 빠르다. 반면 학습용 시뮬레이터는 클래스로 감싸는 편이 안전하다. 우리에게는 **학습이 본업**이니까 후자를 택하자. 단, 이 책 후반의 RISC 챕터에서는 다시 `var`로 돌아갈 수도 있다는 점을 기억해두자. 같은 결정이 챕터마다 다르게 나올 수 있다.

```kotlin
class Register8Test : FunSpec({
    test("초기값은 0이다") {
        Register8().value shouldBe 0
    }

    test("8비트 범위 안의 값은 그대로 들어간다") {
        Register8(0x42).value shouldBe 0x42
        Register8(255).value shouldBe 255
    }

    test("8비트를 넘으면 마스킹된다") {
        Register8(256).value shouldBe 0          // 256 = 0x100 → 마스킹하면 0
        Register8(300).value shouldBe 300 - 256  // 300 - 256 = 44
        Register8(-1).value shouldBe 0xFF        // -1의 비트 패턴은 0xFFFFFFFF → 0xFF
    }

    test("toString은 16진수 두 자리로 패딩한다") {
        Register8(0x4F).toString() shouldBe "0x4F"
        Register8(0x0A).toString() shouldBe "0x0A"
    }
})
```

이 작은 테스트 네 개가 우리의 첫 안전 그물이다. TDD 정신에 따라 `Register8`을 짜기 전에 이 테스트들을 먼저 쓰자. 빨간 줄이 떴다가 초록 줄로 바뀌는 순간, 우리는 그 칸이 약속된 대로 동작한다는 확신을 손에 쥔다.

## 4.2 2의 보수 — 음수를 비트로 적는 약속

가산기를 짜기 전에 한 발 멈춰서 짚어야 할 것이 있다. **음수는 비트로 어떻게 표현되는가?** 이 질문을 정확히 풀지 않으면 곧 만날 뺄셈이 미궁에 빠진다.

방법은 사실 여러 가지다. 부호 비트와 절댓값을 따로 적는 방법(sign-magnitude), 1의 보수, 그리고 우리가 매일 쓰는 2의 보수. 왜 거의 모든 현대 컴퓨터가 **2의 보수**를 택했을까? 한 줄로 답하면, "0이 하나뿐이고, 가산기 하나로 덧셈과 뺄셈을 모두 처리할 수 있어서"다.

2의 보수의 정의는 단순하다. 음수 `-n`은 비트를 모두 뒤집고 1을 더한 값이다. 예를 들어 보자. 8비트에서 `+5`는 `0000 0101`이다. 그러면 `-5`는?

1. 비트를 뒤집는다: `1111 1010`
2. 1을 더한다: `1111 1011`

이게 `-5`의 8비트 표현이다. 16진수로는 `0xFB`다. 이 표현 위에서 `5 + (-5)`를 해보면 어떻게 될까?

```
  0000 0101   (+5)
+ 1111 1011   (-5)
-----------
1 0000 0000   (+0, with carry out)
```

9비트짜리 결과가 나오는데 가장 위 자리가 carry로 떨어져 나가고 8비트 안에는 `0000 0000`만 남는다. 정확히 0이다. 약속이 잘 맞는다.

이 위에서 한 가지 더 짚자. **8비트 2의 보수의 범위는 -128부터 +127까지다.** 가장 위 비트(MSB)가 부호처럼 동작한다 — 0이면 양수, 1이면 음수. 그러면 0과 128(=`1000 0000`)은 어떻게 구별되나? 128을 2의 보수로 해석하면 -128이 된다. 양수 영역은 0부터 127까지(128개), 음수 영역은 -128부터 -1까지(128개), 합쳐서 256개의 값이 들어간다.

> **사이드바: 왜 양수 영역과 음수 영역의 크기가 다른가?**
>
> 양수 영역은 0~127로 128개, 음수 영역은 -128~-1로 128개. 보기에는 대칭처럼 보이지만 살짝 어긋나 있다. 양수 쪽에는 0이 포함되고, 음수 쪽에는 0이 없다. 그래서 -128에 음수 부호를 떼어도 그 절댓값 +128을 8비트 2의 보수로는 표현할 수 없다. `-(-128)` 같은 연산이 입력값 그대로 돌아오는 함정이 여기서 생긴다. 이걸 모르고 짠 절댓값 함수가 자기 함수의 입력값을 그대로 돌려주는 광경을 처음 본 사람의 표정은 정말 난감하다. C99 라이브러리의 `abs(INT_MIN)`도 같은 함정이다.

자, 그러면 SAP-1의 A·B 레지스터에 들어가는 8비트 값들은 양수일까 음수일까? 답은 **둘 다일 수 있다**. 같은 8비트 패턴 `0xFB`를 우리는 "251"로도 읽을 수 있고 "-5"로도 읽을 수 있다. 어느 쪽으로 해석할지는 우리가 그 비트를 어떻게 다루느냐에 달렸다. 덧셈을 할 때는 두 해석 어느 쪽에서도 같은 결과가 나온다 — 이게 2의 보수의 가장 아름다운 성질이다. 가산기 하나로 두 가지 산술을 처리한다.

## 4.3 가산기 — 두 8비트를 더한다

이제 ALU의 가장 기본 동작인 덧셈을 짜 보자. 한 줄로 요약하면 이렇다.

```kotlin
fun add(a: Int, b: Int): Int = (a + b) and 0xFF
```

한 줄이다. 정말 한 줄로 끝난다. JVM의 `Int + Int`가 알아서 32비트 덧셈을 해 주고, `and 0xFF`로 아래 8비트만 자르면 그게 우리 8비트 덧셈의 결과다. 이것이 우리가 고수준 언어에서 시뮬레이터를 짤 때 누리는 호사다 — 하드웨어가 한 사이클에 트랜지스터로 처리하는 일을 JVM의 한 명령어로 흉내낸다.

물론 ALU가 이렇게 끝나면 재미없다. 우리가 짤 ALU는 단순히 합을 내는 게 아니라, **합 + 플래그**를 함께 내야 한다. SAP-1의 플래그는 두 개다 — **Z(zero)**, **C(carry)**. (overflow 플래그 V는 다음 장에서 본격적으로 다룬다. 이 장에서는 일부러 미뤄두자.)

```kotlin
data class AluResult(
    val value: Int,
    val zero: Boolean,
    val carry: Boolean
)

class Alu {
    fun add(a: Int, b: Int): AluResult {
        val aMasked = a and 0xFF
        val bMasked = b and 0xFF
        val raw = aMasked + bMasked       // 9비트까지 자라날 수 있다
        val value = raw and 0xFF          // 아래 8비트만 추린다
        val carry = raw > 0xFF            // 9번째 비트가 살아 있으면 carry
        val zero = value == 0             // 결과가 0이면 Z 플래그
        return AluResult(value, zero, carry)
    }
}
```

여기서 잠깐 멈춰 살펴볼 점이 두 가지 있다.

**첫째, `aMasked = a and 0xFF`로 입력을 한 번 더 자른다.** 호출자가 8비트 약속을 어기고 큰 값을 넣을 수도 있기 때문이다. 방어 코드라고 봐도 좋다. "찜찜한 입력은 일단 자르고 본다"는 정신이다.

**둘째, `carry`는 `raw > 0xFF`로 검출한다.** 9번째 비트가 살아 있다는 것은 8비트 표현이 한 자리 넘쳤다는 뜻이다. 부호 없는 정수의 관점에서 "오버플로우"인 셈인데, **이걸 unsigned overflow 또는 carry**라고 부른다. 부호 있는 정수의 관점에서의 오버플로우는 다른 이야기다 — 그건 다음 장에서.

테스트로 검증해보자.

```kotlin
class AluAddTest : FunSpec({
    val alu = Alu()

    test("기본 덧셈: 3 + 5 = 8, 플래그 모두 false") {
        val r = alu.add(3, 5)
        r.value shouldBe 8
        r.zero shouldBe false
        r.carry shouldBe false
    }

    test("0 + 0 = 0, Z 플래그 true") {
        val r = alu.add(0, 0)
        r.value shouldBe 0
        r.zero shouldBe true
        r.carry shouldBe false
    }

    test("carry 발생: 200 + 100 = 44 (8비트 안), C 플래그 true") {
        val r = alu.add(200, 100)
        r.value shouldBe 44               // 300 - 256
        r.carry shouldBe true
    }

    test("2의 보수 덧셈: +5 + (-5) = 0, Z·C 모두 true") {
        // -5의 8비트 표현은 0xFB
        val r = alu.add(5, 0xFB)
        r.value shouldBe 0
        r.zero shouldBe true
        r.carry shouldBe true             // 9번째 비트가 떨어져 나갔다
    }

    test("255 + 1 = 0 (wrap-around), Z·C 모두 true") {
        val r = alu.add(255, 1)
        r.value shouldBe 0
        r.zero shouldBe true
        r.carry shouldBe true
    }
})
```

다섯 개의 테스트가 가산기의 기본 동작을 모두 잡는다. 특히 네 번째 테스트가 흥미롭다 — `+5 + (-5)`를 했을 때 결과는 0인데 **C 플래그가 켜진다**. "carry가 켜졌으니 오류?" 라고 생각하면 곤란하다. 2의 보수 덧셈에서 carry는 단순히 "9번째 비트가 살아 있었다"는 사실 보고일 뿐, 결과가 틀렸다는 신호가 아니다. 이 미세한 구별이 다음 장의 overflow 플래그를 이해하는 데 결정적이다. 기억해두자.

## 4.4 감산기 — 2의 보수의 트릭

뺄셈은 어떻게 짤까? 정직하게 `a - b`라고 적을 수도 있지만, 진짜 ALU 하드웨어는 그렇게 짜지 않는다. 트랜지스터로 뺄셈 회로를 따로 짜는 것은 비싸다. 그래서 거의 모든 8비트 CPU(8080, 6502, Z80 등)는 **뺄셈을 덧셈으로 환원한다**.

어떻게? `a - b`는 `a + (-b)`와 같다. 그러면 `-b`는 어떻게 만드는가? 2의 보수의 정의 그대로다 — 비트를 뒤집고 1을 더한다.

```
a - b = a + (~b + 1) = a + ~b + 1
```

마지막 `+ 1`을 carry-in으로 처리하면 가산기에 carry 입력 하나만 추가해서 뺄셈을 만들 수 있다. 같은 회로를 덧셈과 뺄셈에 둘 다 쓴다는 점이 너무 우아하다. 이걸 손으로 처음 짚어 본 사람의 표정은 정말 환해진다.

Kotlin으로 옮기면 이렇게 된다.

```kotlin
class Alu {
    fun sub(a: Int, b: Int): AluResult {
        val aMasked = a and 0xFF
        val bMasked = b and 0xFF
        val notB = (bMasked.inv()) and 0xFF      // 비트 뒤집기 (~b)
        val raw = aMasked + notB + 1             // a + ~b + 1
        val value = raw and 0xFF
        val carry = raw > 0xFF                   // carry는 "borrow의 반대"
        val zero = value == 0
        return AluResult(value, zero, carry)
    }
}
```

여기서 `carry` 플래그의 의미를 한 번 더 짚어야 한다. 뺄셈에서 carry는 **"borrow가 없었다"**는 신호다. 8080·6502·Z80은 모두 이 convention을 따른다. `a >= b`이면 carry가 1, `a < b`이면 carry가 0. 헷갈리는 분이 있을 수 있는데, 이건 단순한 컴퓨터 산업의 합의일 뿐이다. 자기 ALU를 짤 때 어느 convention을 따르는지 한 줄 적어두자.

테스트도 함께 짜자.

```kotlin
class AluSubTest : FunSpec({
    val alu = Alu()

    test("기본 뺄셈: 10 - 3 = 7, carry true(borrow 없음)") {
        val r = alu.sub(10, 3)
        r.value shouldBe 7
        r.carry shouldBe true
    }

    test("0 - 1: borrow 발생, 결과 255, carry false") {
        val r = alu.sub(0, 1)
        r.value shouldBe 0xFF             // -1의 8비트 표현
        r.carry shouldBe false            // borrow 발생
        r.zero shouldBe false
    }

    test("3 - 3 = 0, Z 플래그 true, carry true") {
        val r = alu.sub(3, 3)
        r.value shouldBe 0
        r.zero shouldBe true
        r.carry shouldBe true             // borrow 없음
    }
})
```

세 테스트가 충분히 핵심을 잡는다. 256가지 입력 × 256가지 입력 = 65,536가지 케이스 전부를 검증하는 더 본격적인 표 기반 테스트는 다음 장의 overflow와 함께 다루겠다.

## 4.5 정면 결정 — `Int` + 마스킹인가, `UByte`인가?

이쯤에서 우리는 미뤄두었던 큰 질문을 정면으로 마주해야 한다. **8비트 값을 Kotlin에서 무엇으로 표현할 것인가?**

선택지는 사실상 세 가지다. 짧게 정리해보자.

| 선택지 | 장점 | 단점 |
|--------|------|------|
| **`Int` + `and 0xFF` 마스킹** | JVM primitive로 가장 빠름. Java/Scala/Groovy 어디서나 호환. 비트 시프트(`shr`, `shl`) 직접 사용 가능. | 매번 마스킹을 잊으면 부호 확장 버그. 32비트 안에 8비트가 떠다닌다는 의미적 어색함. |
| **`UByte` (Kotlin 1.5+)** | 0~255 자연 표현. `inline class`라 런타임 오버헤드 0. 타입이 약속을 강제한다. | `>>`, `<<` 같은 비트 시프트가 `Byte`/`UByte`에서 **미지원**. `.toInt().shr(n).toUByte()` 변환이 강요된다. |
| **`Byte` (signed -128~127)** | 자바 표준 타입. JNI/serialization 호환. | 자연어와 어긋남. 디버깅 지옥. **추천하지 않는다.** |

세 번째 옵션은 거의 항상 함정으로 떨어진다. `Byte`를 8비트 부호 없는 값으로 다루겠다고 결심하는 순간, 우리는 `Byte.toInt()`가 부호 확장을 일으킨다는 사실과 평생 싸워야 한다. `(0xFF.toByte()).toInt() == -1`이라는 결과를 처음 보면 정말 찜찜하다. 이 길은 가지 말자.

남은 선택지는 두 가지다 — **`Int` + 마스킹**과 **`UByte`**. Kotlin 공식 문서가 이 둘에 대해 직접 답해주는 한 줄이 있다.

> "There is no significant overhead when using unsigned integer types on the JVM. Under the covers, all of the unsigned types in Kotlin are implemented as inline classes."
>
> — Kotlin 공식 문서, *Unsigned integer types*

성능 차이는 없다. 그러면 둘 중 어느 쪽이 더 자연스러운가? 의미만 보면 `UByte` 쪽이 압도적이다. 8비트 부호 없는 값을 표현하기 위한 정확히 그 타입이니까. 그런데 한 가지 함정이 있다.

> "Bit shifts are provided only for UInt and ULong; for the narrower types, both for signed and unsigned, they are under consideration."
>
> — 같은 문서

`UByte`에서는 `shr`, `shl`이 미지원이다. 비트 시프트를 하려면 `.toInt().shr(n).toUByte()` 변환을 거쳐야 한다. 우리가 짤 ALU는 시프트 연산을 자주 쓰는데 매번 이 변환을 끼고 살자면 코드의 호흡이 거칠어진다.

그럼 어떻게 할까? 결정을 내리자. **이 책의 정책은 이렇다.**

> **이 책의 8비트 표현 정책 (4장에서 4부까지)**
>
> - 코드 본문은 `Int` + `and 0xFF` 마스킹으로 간다.
> - 마스킹을 잊지 않기 위해 모든 산술 함수는 `AluResult` 같은 작은 data class로 결과를 감싼다.
> - 메모리는 `IntArray`로 흉내내되, 매 쓰기 시점에 `and 0xFF`로 자른다.
> - **5부(8비트 RISC)에서 `UByte`로 마이그레이션 실험**을 한 챕터 진행하며 차이를 직접 체감한다.

왜 `Int` + 마스킹을 본문 정책으로 택하는가? 세 가지 이유다.

첫째, **가독성**. 비트 시프트와 산술이 모두 정수의 원시 연산으로 자연스럽게 흐른다. 변환의 잡음이 없다.

둘째, **호환성**. Java로 옮기기 쉽다. 학부 강의에서 Java 예제로 변환하는 독자, 회사 시스템에서 자바와 함께 쓰는 독자에게 부담이 적다.

셋째, **실제 사례의 합치**. ksim65 같은 성숙한 Kotlin/JVM CPU 시뮬레이터가 같은 길을 간다. 우리가 처음이 아니라는 점은 결정의 부담을 덜어 준다.

기억해두자. 이 정책은 5부에서 한 번 흔든다. 그때 같은 ALU를 두 가지 표현으로 짜 보고 차이를 손에 새긴다. 그래야 우리가 어떤 트레이드오프 위에 서 있는지 또렷이 보인다.

> **사이드바: Java signed byte의 함정 사례**
>
> 한국 학부 게시판과 OKKY, 그리고 한국 개발자 슬랙 채널에서 가장 자주 보는 byte 함정 사례 셋을 모아두자.
>
> **사례 1.** `byte[] buf = ...; int sum = 0; for (byte b : buf) sum += b;` — 0xFF로 채워진 256바이트 버퍼의 합이 양수가 안 나오고 음수로 떨어진다. 0xFF는 byte로 -1이다. 256개의 -1을 더하면 -256. 입문 면접 단골 함정.
>
> **사례 2.** `byte b = 0x80; int n = b & 0xFF;` — `b & 0xFF`라고 명시적으로 마스킹해야 비로소 부호 확장이 막힌다. `int n = b;`라고만 적으면 `n == -128`이 된다.
>
> **사례 3.** Java InputStream의 `read()`가 `int`를 반환하는 이유. 읽은 바이트는 0~255 사이지만, 스트림이 끝나면 -1을 반환해야 한다. `byte`는 -1도 0xFF도 표현하지만 둘을 구별할 수 없다. 그래서 `int`로 받아 -1과 0~255를 구별한다. API 설계자가 부호 확장의 늪을 한 번 빠져나가 본 사람의 결정이다.
>
> 우리가 `Int` + 마스킹을 택한 이유의 절반이 이 사례 모음 안에 있다. 한 번 데인 사람만이 안다.

## 4.6 논리 연산 — AND, OR, XOR, NOT

이제 ALU에 산술 외의 연산을 더 얹자. SAP-1의 원래 명세에는 논리 연산이 없지만, SAP-2부터는 `ANA`, `ORA`, `XRA`, `CMA`(complement) 같은 명령어가 등장한다. 이 책의 후반 챕터에서 이 명령어들을 만나기 전에, ALU 차원에서 미리 짜 두면 4장과 5장 사이의 호흡이 부드러워진다.

다행히 논리 연산은 Kotlin의 비트 연산자로 거의 즉시 풀린다.

```kotlin
class Alu {
    // 기존 add, sub ...

    fun and(a: Int, b: Int): AluResult {
        val value = (a and b) and 0xFF
        return AluResult(value, value == 0, false)  // 논리 연산은 carry 없음
    }

    fun or(a: Int, b: Int): AluResult {
        val value = (a or b) and 0xFF
        return AluResult(value, value == 0, false)
    }

    fun xor(a: Int, b: Int): AluResult {
        val value = (a xor b) and 0xFF
        return AluResult(value, value == 0, false)
    }

    fun not(a: Int): AluResult {
        val value = (a.inv()) and 0xFF
        return AluResult(value, value == 0, false)
    }
}
```

논리 연산은 carry가 의미 없다 — 자릿수가 넘어가는 일이 없으니까. 그래서 C 플래그는 그냥 false로 둔다. Z 플래그는 여전히 유효하다. 결과가 0인지 아닌지를 따지는 명령어가 곧 분기 명령어(JZ/JNZ)의 조건으로 쓰이기 때문이다.

테스트 몇 개를 함께 짜자.

```kotlin
class AluLogicTest : FunSpec({
    val alu = Alu()

    test("AND: 0x0F and 0xAA = 0x0A") {
        alu.and(0x0F, 0xAA).value shouldBe 0x0A
    }

    test("OR: 0xF0 or 0x0F = 0xFF") {
        alu.or(0xF0, 0x0F).value shouldBe 0xFF
    }

    test("XOR으로 자기 자신을 지운다: a xor a == 0") {
        alu.xor(0x42, 0x42).let {
            it.value shouldBe 0
            it.zero shouldBe true
        }
    }

    test("NOT: ~0xAA = 0x55") {
        alu.not(0xAA).value shouldBe 0x55
    }

    test("논리 연산은 carry를 켜지 않는다") {
        alu.and(0xFF, 0xFF).carry shouldBe false
        alu.or(0xFF, 0xFF).carry shouldBe false
    }
})
```

`XOR으로 자기 자신을 지운다`는 사례는 80년대 어셈블리어 코드에서 진짜 자주 보던 관용구다. `XOR AX, AX`는 `MOV AX, 0`보다 한 바이트 짧고 한 사이클 빠르다. 그래서 80년대 x86 코드는 레지스터를 0으로 만들 때 거의 항상 XOR를 썼다. 이 관용구가 어떻게 일하는지가 ALU 차원에서 손에 잡혀 있어야 11장에서 Fibonacci 코드를 4가지 어셈블리로 비교할 때 자연스럽게 해석된다.

> **사이드바: 6502는 왜 XOR를 EOR라고 부르나?**
>
> 같은 연산이 CPU마다 이름이 다르다. 8080·8086 계열은 `XOR`, 6502는 `EOR`(Exclusive OR), 6800도 `EOR`. 본질은 같은 비트 연산이지만 어셈블리 이름은 그 칩을 설계한 회사의 전통에 따라 갈렸다. 이런 이름의 갈래가 11장 ISA 비교에서 또렷이 보일 것이다. 같은 일을 다른 단어로 부르는 그 다양함이 8비트 시대의 매력이다.

## 4.7 데이터패스 그림으로 정리

ALU와 레지스터를 다 짰으니, SAP-1의 데이터패스에서 이 둘이 어떻게 묶이는지를 한 번 그려보자. 실제 모듈 통합은 6장이지만, 그림으로 미리 그려두면 다음 두 장의 흐름이 잘 보인다.

```
              ┌──────────────┐
              │   A 레지스터  │ ◄──── W-bus ────┐
              │   (8비트)    │                  │
              └──────┬───────┘                  │
                     │                          │
                     ▼                          │
              ┌──────────────┐                  │
              │     ALU      │                  │
              │  add/sub/    │                  │
              │  and/or/xor  │ ───── W-bus ────►│
              │              │                  │
              └──────▲───────┘                  │
                     │                          │
              ┌──────┴───────┐                  │
              │   B 레지스터  │ ◄──── W-bus ────┘
              │   (8비트)    │
              └──────────────┘
                     │
                     ▼
              ┌──────────────┐
              │ 플래그 레지스터│
              │  Z, C (4장)   │
              │  V, S (5장)   │
              └──────────────┘
```

W-bus가 모든 모듈을 하나의 통로로 묶는 모습이 보일 것이다. A와 B에서 값이 ALU로 흘러 들어가고, 연산 결과가 다시 W-bus로 돌아온다. 플래그 레지스터는 그 옆에 따로 앉아서 연산의 부산물을 기록한다. 6장에서 이 그림을 컨트롤러로 살린다. 그때까지는 이 그림이 우리 머릿속의 지도다.

## 4.8 한 챕터를 마치며

이번 장에서 우리가 손에 쥔 것을 정리해보자.

첫째, **레지스터를 `Register8` 클래스로 감쌌다.** setter에서 자동으로 `and 0xFF` 마스킹을 한다. 이 작은 보호막 하나가 디버깅을 크게 편하게 해 준다.

둘째, **2의 보수의 동작을 손으로 짚었다.** 음수는 비트를 뒤집고 1을 더해 만든다. 8비트 범위는 -128부터 +127까지. 가산기 하나로 덧셈과 뺄셈을 모두 처리할 수 있다는 이 한 줄 위에 8비트 시대의 산술이 모두 서 있다.

셋째, **ALU의 가산기·감산기·논리 연산을 모두 짰고 테스트했다.** Z·C 플래그까지. overflow 플래그 V는 다음 장의 핵심으로 남겨두었다.

넷째 — 이게 가장 무거운 결정이었다 — **이 책의 8비트 표현 정책을 `Int` + 마스킹으로 정했다.** 5부에서 한 번 흔들기로 약속했다. 그때까지는 이 정책을 기준으로 코드를 짜자. 일관된 기준 위에서만 비교 실험의 결과가 또렷이 보인다.

기억해두자. **2의 보수의 carry와 overflow는 다른 개념이다.** 둘을 혼동하면 다음 장의 90% 입문자 무덤에서 함께 묻힌다. carry는 부호 없는 관점에서의 자릿수 넘침이고, overflow는 부호 있는 관점에서의 부호 뒤집힘이다. 둘이 같은 비트 패턴에서 서로 다른 진실을 본다. 다음 장은 정확히 이 차이를 정면돌파한다.

자, 다음 장으로 가 보자. **overflow라는 무덤**으로.

> **GitHub 산출물**
>
> - 파일: `chapter-04/sap1/Register.kt`, `chapter-04/sap1/Alu.kt`
> - 테스트: `chapter-04/sap1/RegisterTest.kt`(4개), `chapter-04/sap1/AluTest.kt`(약 30개 — add 5, sub 3~5, and/or/xor/not 합쳐서 ~10개, 마스킹·flag 회귀 ~10개)
> - 실행 커맨드: `./gradlew :chapter-04:test`
> - 다음 장에서 이 ALU에 overflow 플래그와 표 기반 테스트(256×256×2 = ~131,072 케이스)를 얹는다.
