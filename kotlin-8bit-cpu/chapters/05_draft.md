# 5장. overflow라는 무덤 — ADC/SBC를 테스트로 잡는다

8비트 emulator를 짜다가 망한 사람의 글을 충분히 많이 읽어보면, 어느 순간 한 가지 단어가 자주 등장한다는 걸 알게 된다. **overflow**다. Reddit의 r/emulation, Stack Overflow의 6502 태그, NESdev 포럼, HN의 emulator 후기. 사람들은 "처음에는 잘 돌았는데, 어느 순간 게임의 점수 계산이 어긋나기 시작했다"고 호소한다. 디버거를 들고 추적해보면 ADC 명령어 한 줄에서 V 플래그가 잘못 떨어진다. 게임은 그 V 플래그를 보고 분기한다. 결과는 알 수 없는 곳으로의 점프다. 디버깅에 사흘이 사라진다.

왜 하필 overflow일까? 8비트 가산기 자체는 어렵지 않다. 4학년 산수를 비트로 옮긴 것에 가깝다. 그런데 그 가산기에 매달린 작은 1비트 플래그 하나가 입문자의 발목을 잡는다. Ken Shirriff가 자기 블로그에 6502 overflow 해설을 올렸을 때, "10년 만에 처음으로 이 플래그가 이해됐다"는 댓글이 줄을 이었다. 정말 그 정도다.

그렇다면 우리도 그 무덤을 피할 수 없는가? 다행히 답이 있다. **테스트로 잡는다.** 손으로 한 번 계산하기 어려운 것이라면, 한 번 정한 공식을 256 × 256 × 2 = 131,072개의 케이스에 자동으로 들이대 본다. 잘못된 부분이 있으면 빨간 줄이 즉시 알려준다. 이 챕터는 그 길을 직접 걷는 챕터다. ALU에 SF(sign)와 OF(overflow) 플래그를 추가하고, kotest를 설치해 표 기반 테스트와 property-based test로 정면 돌파한다. 여기를 넘으면 8비트 CPU의 절반은 끝났다고 봐도 좋다. 함께 가보자.

## 2의 보수 — 빼기를 더하기로 만드는 마법

overflow 이야기를 하기 전에 한 번 짚어둘 것이 있다. **2의 보수**다. 4장에서 가산기를 짜면서 슬쩍 등장했지만, 이번에는 정면으로 봐야 한다. overflow 플래그의 정체가 바로 이 표현 방식의 그림자이기 때문이다.

8비트 부호 있는 정수는 -128부터 127까지를 표현한다. 그런데 컴퓨터의 회로 안에서는 이게 어떻게 살까? 음수를 어떻게 표현할까? 가장 자연스러워 보이는 후보가 두 가지 있다.

첫째, **부호-크기 표현(sign-magnitude)**. 최상위 비트를 부호 비트로 쓰고, 나머지 7비트를 크기로 쓴다. `0000 0001`이 +1, `1000 0001`이 -1이다. 인간에게는 직관적이다. 그러나 회로는 비명을 지른다. 왜 그럴까? **0이 두 개**다. `0000 0000`(+0)과 `1000 0000`(-0). 비교 회로가 이 둘을 같은 0으로 간주하려면 별도의 분기가 필요하다. 게다가 덧셈 회로가 부호를 보고 분기해야 한다. 같은 부호면 더하고, 다른 부호면 빼야 한다. 회로가 두 배로 복잡해진다. 끔찍한 일이다.

둘째, **1의 보수(one's complement)**. 음수는 그냥 비트를 반전한다. `0000 0001`이 +1이면 `1111 1110`이 -1이다. 덧셈은 그냥 더하면 된다는 점에서 회로가 단순해진다. 그러나 여전히 0이 두 개다(`0000 0000`과 `1111 1111`). 그리고 "end-around carry"라는 특이한 처리가 필요하다.

그래서 등장한 것이 **2의 보수**다. 음수를 만드는 법은 단순하다. **비트를 모두 반전한 뒤 1을 더한다**. -1을 만들어보자.

```
  +1: 0000 0001
반전: 1111 1110
+1:   1111 1111  ← 이게 -1
```

-128은 어떨까?

```
+128: (8비트로는 표현 불가, 0~127만 양수)
+127: 0111 1111
+128에 해당하는 것을 만들기 위해 1을 더 더하면 ...
-128: 1000 0000
```

2의 보수가 가져다주는 마법이 무엇인지 보자.

| 표현 | 부호 있는 해석 | 부호 없는 해석 |
|------|----------------|----------------|
| `0000 0000` | 0 | 0 |
| `0000 0001` | +1 | 1 |
| `0111 1111` | +127 | 127 |
| `1000 0000` | -128 | 128 |
| `1111 1110` | -2 | 254 |
| `1111 1111` | -1 | 255 |

**0이 하나뿐이다.** 비교 회로가 단순해진다. 더하기 회로 하나로 빼기도 처리할 수 있다. -1과 +1을 더하면 `1111 1111 + 0000 0001 = 1 0000 0000`이고, 8비트만 남기면 정확히 `0000 0000` = 0이다. 별도 처리 없이 그냥 더했더니 정답이 나왔다. 회로 설계자에게 이건 거의 시 같은 발견이었다.

그렇다면 의문이 든다. **빼기는 어떻게 하나?** A - B를 계산하고 싶을 때, B의 2의 보수(반전 후 +1)를 만들어 A에 더한다.

```
  5 -  3 =  2 를 계산해보자.
  5: 0000 0101
  3: 0000 0011
  
  -3 만들기:
    3 반전: 1111 1100
    +1:     1111 1101  ← 이게 -3
  
  5 + (-3):
    0000 0101
  + 1111 1101
  ─────────────
  1 0000 0010   ← 9비트가 됐지만 상위 1은 버리면 0000 0010 = 2 ✓
```

그래서 SAP-1이나 6502 같은 8비트 CPU의 SUB 명령어는 내부적으로 ADD를 약간 변형해 만든다. **빼기는 더하기의 한 변형**이다. 이 사실 하나가 8비트 ALU의 가장 우아한 부분이다. 그러나 이 우아함이 끝나는 자리에 overflow가 기다리고 있다.

## C 플래그와 V 플래그 — 두 가지 다른 거짓말

자, 이제 정면으로 가자. **C(carry) 플래그**와 **V(overflow) 플래그**는 둘 다 "더하기 결과가 8비트로는 부족해졌다"를 알리는 신호다. 그런데 둘은 같은 신호가 아니다. **서로 다른 두 가지 거짓말**을 알린다.

| 플래그 | 알리는 것 | 의미가 있는 해석 |
|--------|-----------|------------------|
| C (carry) | 9번째 비트로 올림이 생겼나? | **부호 없는 수**의 overflow |
| V (overflow) | 부호 비트가 잘못 바뀌었나? | **부호 있는 수**의 overflow |

처음 듣는 사람은 분명 어리둥절할 것이다. "그게 둘 다 같은 거 아닌가?" 절대 그렇지 않다. 같은 ADD 한 번에 둘이 따로따로 0/1을 갖는다. 직접 보자.

### 사례 1 — `200 + 100`

부호 없는 수로 보면 200 + 100 = 300이지만, 8비트는 255까지밖에 못 담는다. 부호 없는 해석으로 overflow가 났다.

```
  200: 1100 1000
  100: 0110 0100
─────────────────
       1 0010 1100   ← 9비트째에 1이 올라갔다
       C=1
       
8비트만 남기면 0010 1100 = 44
```

C는 1. 부호 없는 해석으로는 "200 + 100 = 44"라고 답한 셈이다. 거짓이다.

그런데 같은 비트열을 **부호 있는 수**로 다시 읽어보자.

```
  200을 부호 있는 8비트로 읽으면? 1100 1000은 최상위 비트가 1이므로 음수.
  반전 + 1: 0011 0111 + 1 = 0011 1000 = 56. 그러므로 200(unsigned) = -56(signed).
  100은 양수 그대로 100.
  
  부호 있는 덧셈: -56 + 100 = 44. 
  
  결과 0010 1100을 부호 있는 수로 읽으면? 최상위 0이므로 양수 그대로 44. 정답!
```

부호 있는 해석으로는 답이 맞다. V는 0이다.

### 사례 2 — `100 + 100`

부호 없는 수로 보면 200. 8비트에 들어간다. C는 0. 그런데 부호 있는 수로 보면 100 + 100 = 200이고, 부호 있는 8비트는 +127까지만 표현한다. 부호 있는 해석으로 overflow.

```
  100: 0110 0100
  100: 0110 0100
─────────────────
       1100 1000   ← 8비트 안에 들어갔지만, 부호 비트가 0에서 1로 뒤집혔다
       C=0, V=1
       
부호 없는 해석: 100 + 100 = 200 ✓
부호 있는 해석: +100 + +100 = -56 ✗ (실제 결과 1100 1000을 부호 있는 수로 읽으면 -56)
```

같은 덧셈 한 번에 C와 V가 다른 답을 내고 있는 것이 보이는가? **C는 부호 없는 수의 진실성을, V는 부호 있는 수의 진실성을 따로 추적한다.** 그래서 어셈블리 프로그래머는 자기 코드가 부호 있는 수를 다루는지 부호 없는 수를 다루는지에 따라 다른 분기 명령어를 쓴다. BCC/BCS는 C를, BVC/BVS는 V를 본다. 한쪽을 다른 쪽으로 잘못 쓰면 게임은 미궁으로 점프한다.

여기서 더 깊은 의문이 든다. **V 플래그는 정확히 어떻게 계산하는가?**

## V 플래그 — Ken Shirriff의 한 줄 공식

V 플래그를 처음 만나면 누구나 비슷한 시도를 한다. "결과가 +127보다 크면 1, -128보다 작으면 1"이라고. 그런데 회로 안에는 "결과가 +127보다 크다"를 판단할 수단이 없다. 비교 자체가 별도 회로다. 더 단순한 방법이 있어야 한다.

답은 충격적으로 단순하다. **두 피연산자의 부호 비트가 같은데, 결과의 부호 비트가 다르면 overflow다.**

말이 길다. 표로 정리해보자.

| A의 부호 | B의 부호 | 결과의 부호 | overflow? |
|---------|---------|-------------|-----------|
| + | + | + | 0 |
| + | + | - | **1** |
| + | - | + | 0 |
| + | - | - | 0 |
| - | + | + | 0 |
| - | + | - | 0 |
| - | - | + | **1** |
| - | - | - | 0 |

논리는 자명하다. **양수 + 양수는 절대 음수가 될 수 없다.** 음수 + 음수는 절대 양수가 될 수 없다. 그런데 비트 차원에서 그런 일이 일어났다면, 그건 회로의 거짓말이다. 부호 비트가 뒤집혔다. 그게 overflow다.

부호가 다른 두 수의 덧셈은? overflow가 절대 발생하지 않는다. 절댓값이 작아지는 방향이기 때문이다. 직관적으로 납득된다.

Ken Shirriff의 6502 분석에 따르면, 이 공식은 한 줄 XOR로 떨어진다.

```
V = (A_sign XOR result_sign) AND (B_sign XOR result_sign)
  = ((A XOR result) AND (B XOR result)) of bit 7
```

같은 부호의 두 수를 더했는데(즉 `A_sign == B_sign`) 결과의 부호가 둘과 다르다면 V가 1이 된다. 이 한 줄이 V 플래그의 정체다. **이걸 한 번 손에 익히면 다시는 헷갈리지 않는다**.

### SBC의 경우

SUB(또는 6502의 SBC, "Subtract with Carry")의 V 플래그는 살짝 다르다. 빼기는 더하기의 변형이라 했다. A - B = A + (~B + 1). 따라서 B의 부호 비트가 반전된 상태로 들어간다. V 공식도 약간 바뀐다.

```
V = ((A XOR result) AND ((~B) XOR result)) of bit 7
  = ((A XOR result) AND ((B XOR result XOR 1))) of bit 7
```

말이 복잡해 보이지만 핵심은 같다. **A와 ~B(빼는 수의 반전)의 부호가 같은데, 결과 부호가 다르면 overflow.** 부호가 같은 두 수를 더하는 것과 본질적으로 동일한 상황이기 때문이다.

이 한 줄을 종이에 적어두자. 코드를 짜면서 모니터 옆에 붙여두자. ADC/SBC를 짤 때마다 들춰볼 것이다. 익숙해질 때까지는.

## ALU 클래스에 플래그 추가하기

이제 4장에서 짠 ALU에 SF와 OF를 추가하자. 4장 끝의 ALU는 Z(zero)와 C(carry) 두 플래그만 들고 있었을 것이다. 거기에 SF(sign, 결과가 음수인가)와 OF(overflow)를 더한다.

먼저 데이터 구조를 정리한다. 결과와 플래그를 한 묶음으로 들고 다니기 위해 data class를 쓰자.

```kotlin
// chapter-05/sap1/AluResult.kt
data class AluResult(
    val value: Int,    // 8비트로 마스킹된 결과
    val z: Boolean,    // zero
    val c: Boolean,    // carry (부호 없는 overflow)
    val s: Boolean,    // sign (결과의 최상위 비트)
    val v: Boolean     // overflow (부호 있는 overflow)
)
```

플래그 네 개가 한 인스턴스에 묶여 있다. ALU의 메서드는 이 구조체 하나를 돌려준다. 그러면 호출하는 쪽이 "결과는 받았는데 플래그는 어디에?" 하는 일이 없다. 작은 안전판이다.

ALU 본체는 이렇게 확장한다.

```kotlin
// chapter-05/sap1/Alu.kt
class Alu {

    fun add(a: Int, b: Int, carryIn: Boolean = false): AluResult {
        val ai = a and 0xFF
        val bi = b and 0xFF
        val cin = if (carryIn) 1 else 0
        val raw = ai + bi + cin            // 9비트까지 갈 수 있음
        val result = raw and 0xFF

        val c = (raw and 0x100) != 0
        val z = result == 0
        val s = (result and 0x80) != 0
        // V = (A와 결과의 부호가 다르고) AND (B와 결과의 부호가 다르다)
        val v = (((ai xor result) and (bi xor result)) and 0x80) != 0

        return AluResult(result, z, c, s, v)
    }

    fun sub(a: Int, b: Int, borrowIn: Boolean = false): AluResult {
        // A - B - borrow = A + (~B and 0xFF) + (1 - borrow)
        val ai = a and 0xFF
        val bi = b and 0xFF
        val borrow = if (borrowIn) 0 else 1   // 6502 스타일: carry=1이면 borrow 없음
        val notB = bi.inv() and 0xFF
        val raw = ai + notB + borrow
        val result = raw and 0xFF

        // SUB에서 C는 "borrow가 없었나?"를 알린다 (6502 관행)
        val c = (raw and 0x100) != 0
        val z = result == 0
        val s = (result and 0x80) != 0
        val v = (((ai xor result) and (notB xor result)) and 0x80) != 0

        return AluResult(result, z, c, s, v)
    }
}
```

V 플래그 계산이 이 한 줄에 응축돼 있다.

```kotlin
val v = (((ai xor result) and (bi xor result)) and 0x80) != 0
```

비트 7만 봐서 0인지 아닌지를 따진다. 두 피연산자의 부호와 결과의 부호가 같이 뒤집혔는지를 한 번에 체크하는 셈이다. 이 짧은 줄이 며칠을 잡아먹게 만드는 함정이라는 점이 새삼 신기하다.

### SBC의 borrow 규약 — 6502와 같은 길로 간다

SBC에서 한 가지 짚고 갈 것이 있다. **carry-in의 의미가 ADC와 다르다.** 6502 관행은 다음과 같다.

- ADC: carry-in이 1이면 결과에 1을 더 더한다(multi-byte 덧셈에서 이전 자리의 올림)
- SBC: carry-in이 1이면 borrow가 없다(이전 자리에서 빌려가지 않았다). 0이면 borrow가 있다.

처음 보면 살짝 거꾸로 같다. 그러나 잘 보면 일관성이 있다. **C 플래그는 "정상 동작"을 1로 표기한다**. ADC에서는 "정상적으로 캐리가 발생"이면 1, SBC에서는 "정상적으로 borrow 없이 빠짐"이면 1. 이걸 따라가는 편이 이후 multi-byte 산술의 흐름이 자연스러워진다. SAP-1은 multi-byte 산술이 없지만, 이 규약을 처음부터 따라두면 SAP-2와 우리의 8비트 RISC에서 그대로 쓸 수 있다. 미래에 자신에게 보내는 작은 선물이다.

## kotest 설치 — 본격적인 테스트 전략의 시작

코드는 짰다. 그런데 진짜 어려운 건 지금부터다. **이게 정말로 맞는지를 어떻게 확인할 것인가?** 손으로 짚어볼 수 있는 케이스는 한 자릿수다. 그러나 V 플래그 공식이 모든 부호 있는 8비트 입력에 대해 옳다고 어떻게 확신할까?

답은 **모든 케이스를 다 돌려보는 것**이다. 부호 있는 8비트 × 부호 있는 8비트 × carry 2가지 = 131,072 조합. 사람은 못 한다. 컴퓨터는 한순간에 한다. 그래서 8비트 emulator 커뮤니티는 처음부터 테스트 ROM을 신화처럼 떠받든다.

| 프로젝트 | 검증 도구 | 비고 |
|----------|----------|------|
| 6502 | klaus2m5/6502_65C02_functional_tests | 6502 emulator의 사실상 표준 |
| NES | nestest.nes | 카트리지 자체가 self-test |
| Chip-8 | Timendus' test suite | 빠르고 가시적 |
| GameBoy | Blargg's test ROMs | cycle-accurate 검증에까지 사용 |

> "There's a program from 6502.org that verifies 6502 Overflow (V) Flag behavior, which tests both ADC and SBC instructions with all 256 possible values for both operands and different carry flag states." — 커뮤니티-휴리스틱3

SAP-1에는 이런 외부 ROM이 없다. **그러니 우리가 직접 만든다.** 우리의 도구는 Kotlin과 kotest다. kotest는 JUnit과 호환되면서도 표 기반 테스트(table-driven test)와 property-based test를 깔끔하게 지원한다. 이 챕터에서 본격 도입하자.

`build.gradle.kts`에 의존성을 추가한다.

```kotlin
// chapter-05/build.gradle.kts
plugins {
    kotlin("jvm") version "1.9.22"
}

dependencies {
    testImplementation("io.kotest:kotest-runner-junit5:5.8.0")
    testImplementation("io.kotest:kotest-property:5.8.0")
    testImplementation("io.kotest:kotest-assertions-core:5.8.0")
}

tasks.test {
    useJUnitPlatform()
}
```

여기서 잠깐 멈춰서 묻자. **JUnit5만 써도 되지 않나?** 물론 그래도 된다. `@ParameterizedTest`로 비슷한 일을 할 수 있다. 그러나 kotest의 두 가지 장점이 결국 마음을 끈다. 첫째, DSL이 자연스럽다. 한국어로 옮긴 듯한 BDD 스타일이 가능하다. 둘째, **property-based test**가 일등 시민이다. 무작위 입력 1000개로 명령어의 invariant를 검증하는 도구가 표준 라이브러리에 들어 있다. 8비트 산술처럼 입력 공간이 작은 영역에서는 이게 결정적인 무기가 된다. ksim65도 같은 길을 갔다.

## 표 기반 테스트 — 손으로 정한 진실의 닻

먼저 손으로 정한 케이스부터 가자. **이것만은 절대 맞아야 한다**는 진실의 닻을 표로 박아둔다. 이게 무너지면 ALU의 의미가 무너지는 그런 케이스들이다.

```kotlin
// chapter-05/sap1/AluAddTest.kt
import io.kotest.core.spec.style.FunSpec
import io.kotest.data.forAll
import io.kotest.data.row
import io.kotest.matchers.shouldBe

class AluAddTest : FunSpec({

    val alu = Alu()

    context("ADD 핵심 케이스") {
        forAll(
            //     A    B    cin    result   z      c      s      v
            row(  0,   0, false,    0,    true,  false, false, false),
            row(  1,   1, false,    2,    false, false, false, false),
            row(127,   1, false,  128,    false, false, true,  true ),  // +127+1 = -128, V!
            row(127, 127, false,  254,    false, false, true,  true ),  // +127+127 = -2, V!
            row(255,   1, false,    0,    true,  true,  false, false),  // 255+1 = 0, C!
            row(200, 100, false,   44,    false, true,  false, false),  // unsigned overflow only
            row(100, 100, false,  200,    false, false, true,  true ),  // signed overflow only
            row(128, 128, false,    0,    true,  true,  false, true ),  // -128 + -128 = 0, C and V
            row( 50,  50, true,   101,    false, false, false, false),  // carry-in 적용
        ) { a, b, cin, expectedResult, z, c, s, v ->
            val r = alu.add(a, b, cin)
            r.value shouldBe expectedResult
            r.z shouldBe z
            r.c shouldBe c
            r.s shouldBe s
            r.v shouldBe v
        }
    }
})
```

이 한 블록에 아홉 개의 단언이 들어 있다. **각 행이 V 플래그의 한 모서리를 짚는다.** `127 + 1 = 128`이 부호 있는 해석으로는 -128, 즉 부호가 뒤집힌 V=1 케이스. `128 + 128`은 부호 있는 해석으로 `-128 + -128 = -256`이고 8비트로는 0이며, V=1, C=1이 같이 떨어진다. 이런 모서리 케이스 아홉 개가 우리의 진실의 닻이다.

이 표가 빨갛게 되면 무언가 큰 게 깨진 거다. 잠깐 멈추고 들여다본다. 작은 회귀라면 표가 작아 디버깅이 빠르다. 표 기반 테스트의 미덕은 **실패 메시지가 행 단위로 떨어진다**는 점이다. 어느 행이 깨졌는지가 한눈에 보인다. 디버깅 한나절을 살리는 작은 사치다.

SUB도 같은 패턴으로 표를 짠다.

```kotlin
// chapter-05/sap1/AluSubTest.kt
class AluSubTest : FunSpec({

    val alu = Alu()

    context("SUB 핵심 케이스") {
        forAll(
            //      A     B   borrowIn  result   z      c      s      v
            row(   5,    3, false,        2,    false, true,  false, false),
            row(   3,    5, false,      254,    false, false, true,  false),  // 3-5 = -2
            row(   0,    0, false,        0,    true,  true,  false, false),
            row(   0,    1, false,      255,    false, false, true,  false),  // 0-1 = -1, borrow!
            row(-128,    1, false,      127,    false, true,  false, true ),  // -128 - 1 = +127! V
            row( 127,   -1, false,      128,    false, false, true,  true ),  // +127 - (-1) = -128! V
            row(  10,    5, true,         4,    false, true,  false, false),  // borrow-in 적용
        ) { a, b, bIn, expectedResult, z, c, s, v ->
            val r = alu.sub(a and 0xFF, b and 0xFF, bIn)
            r.value shouldBe expectedResult
            r.z shouldBe z
            r.c shouldBe c
            r.s shouldBe s
            r.v shouldBe v
        }
    }
})
```

`-128 - 1`이 부호 있는 8비트에서 +127로 떨어지는 케이스가 SBC의 V를 보여주는 정수다. **부호 있는 수의 한쪽 끝(-128)에서 빼려고 했더니 반대편 끝(+127)으로 점프했다.** 이게 V=1의 의미다.

## Property-based test — 무작위로 진실을 시험한다

표 기반 테스트로 핵심 케이스는 잡았다. 그러나 256 × 256 × 2 = 131,072개 전부를 손으로 적을 수는 없다. 여기서 property-based test가 등장한다. **무작위 입력에 대해 항상 성립해야 하는 속성**을 정의하고, 라이브러리가 입력을 자동으로 생성해 검증한다.

ALU의 핵심 invariant 몇 가지를 골라보자.

1. **덧셈의 결과는 항상 8비트 안에 들어간다** (마스킹 자체의 안정성)
2. **Z 플래그는 결과가 0일 때만 1이다**
3. **부호가 다른 두 수의 덧셈은 V가 절대 1이 아니다**
4. **A + 0 = A** (덧셈의 항등원)
5. **부호 없는 수의 진실: (a + b) mod 256 == result, 그리고 (a + b) >= 256 == C**

이걸 kotest로 옮긴다.

```kotlin
// chapter-05/sap1/AluPropertyTest.kt
import io.kotest.core.spec.style.FunSpec
import io.kotest.matchers.shouldBe
import io.kotest.property.Arb
import io.kotest.property.arbitrary.int
import io.kotest.property.arbitrary.boolean
import io.kotest.property.checkAll

class AluPropertyTest : FunSpec({

    val alu = Alu()

    test("덧셈 결과는 항상 0..255 범위에 있다") {
        checkAll(Arb.int(0..255), Arb.int(0..255), Arb.boolean()) { a, b, cin ->
            val r = alu.add(a, b, cin)
            (r.value in 0..255) shouldBe true
        }
    }

    test("Z 플래그는 결과가 0일 때만 1이다") {
        checkAll(Arb.int(0..255), Arb.int(0..255), Arb.boolean()) { a, b, cin ->
            val r = alu.add(a, b, cin)
            r.z shouldBe (r.value == 0)
        }
    }

    test("부호가 다른 두 수의 덧셈은 V가 0이다") {
        checkAll(Arb.int(0..127), Arb.int(128..255)) { aPos, bNeg ->
            // aPos는 부호 비트 0, bNeg는 부호 비트 1
            val r = alu.add(aPos, bNeg, false)
            r.v shouldBe false
        }
    }

    test("A + 0 = A") {
        checkAll(Arb.int(0..255)) { a ->
            val r = alu.add(a, 0, false)
            r.value shouldBe a
        }
    }

    test("unsigned overflow 진실: (a+b)>=256 <-> C=1") {
        checkAll(Arb.int(0..255), Arb.int(0..255)) { a, b ->
            val r = alu.add(a, b, false)
            val rawSum = a + b
            r.c shouldBe (rawSum >= 256)
            r.value shouldBe (rawSum and 0xFF)
        }
    }
})
```

각 테스트가 기본적으로 1000개의 무작위 입력을 돌린다. 5,000 × 5 = 25,000건의 검증이 단위 테스트 한 번에 일어난다. 표 기반 테스트로 잡은 9개 케이스 + property test 25,000건. ALU의 invariant가 무너지면 거의 확실하게 한 번에 잡힌다.

> **사이드바: property-based test의 함정**
>
> property-based test는 강력하지만 가끔 사람을 속인다. 무작위 입력이 운 좋게(혹은 운 나쁘게) 함정을 다 비껴갈 수 있다. **꼭 표 기반의 진실의 닻과 함께 쓰자**. property test가 "1000개 다 통과했다"고 알려도, `127 + 1` 같은 모서리 케이스를 손으로 정한 표에 박아두지 않으면 어느 날 슬그머니 깨진다. 둘은 서로의 보완재지 대체재가 아니다. 이걸 잊으면 정말로 찜찜한 일이 벌어진다.
>
> kotest의 `Arb.int(0..255)`는 단순 균등 분포 외에도 edge case를 우선 시도하는 모드가 있다. `Arb.int(0..255).withEdgecases(listOf(0, 1, 127, 128, 255))` 식으로 명시하면 매 실행마다 모서리부터 시도한다. 한 단계 더 안전한 안전망이다.

## 256 × 256 × 2 = 131,072 — 전수조사를 해버리자

`Arb.int`를 쓰면 1000개씩 샘플링하지만, 8비트 산술에서는 사실 **전수조사가 가능하다**. 입력 공간이 작기 때문이다. 한 번 더 안전망을 깐다.

```kotlin
// chapter-05/sap1/AluExhaustiveTest.kt
import io.kotest.core.spec.style.FunSpec
import io.kotest.matchers.shouldBe

class AluExhaustiveTest : FunSpec({

    val alu = Alu()

    test("ADD: 256 x 256 x 2 = 131,072 전수조사") {
        for (a in 0..255) {
            for (b in 0..255) {
                for (cin in listOf(false, true)) {
                    val r = alu.add(a, b, cin)
                    val raw = a + b + (if (cin) 1 else 0)

                    // value 검증
                    r.value shouldBe (raw and 0xFF)

                    // C 검증
                    r.c shouldBe (raw > 255)

                    // Z 검증
                    r.z shouldBe (r.value == 0)

                    // S 검증
                    r.s shouldBe (r.value >= 128)

                    // V 검증 (참조 공식: 부호 있는 결과가 -128..127 범위를 벗어났나)
                    val sA = if (a < 128) a else a - 256
                    val sB = if (b < 128) b else b - 256
                    val sCin = if (cin) 1 else 0
                    val signedRaw = sA + sB + sCin
                    val signedOverflow = signedRaw < -128 || signedRaw > 127
                    r.v shouldBe signedOverflow
                }
            }
        }
    }
})
```

이 한 테스트가 131,072개의 단언을 실행한다. 그런데 JVM에서 1초가 채 안 걸린다. CPU 입장에서 13만 번의 정수 연산은 한순간이다. **8비트의 비좁음이 우리에게 주는 가장 큰 선물이 바로 이 전수조사 가능성이다.** SAP-1이 16바이트라는 점에 답답해하던 독자에게 위안의 거울이다.

여기서 한 가지 의문이 들 수 있다. **참조 공식을 자기가 구현해서 자기가 검증하는 게 무슨 의미인가?** 좋은 질문이다. 답은 이렇다. **참조 공식과 실제 구현은 다른 방식으로 짜야 의미가 있다**. 위의 V 검증은 "부호 있는 산술 결과가 8비트 부호 있는 범위를 벗어났나"라는 **사람이 이해하기 쉬운 형태**로 짰고, ALU 본체는 **회로가 실제로 하는 비트 XOR**로 짰다. 두 방식이 같은 답을 내야 한다는 사실이 검증이다. 의미론적 공식과 비트 공식이 서로의 거울이 되는 것. 이게 emulator 테스트의 가장 강력한 패턴이다.

## SUB도 동일하게 전수조사

```kotlin
test("SUB: 256 x 256 x 2 = 131,072 전수조사") {
    for (a in 0..255) {
        for (b in 0..255) {
            for (bIn in listOf(false, true)) {
                val r = alu.sub(a, b, bIn)
                val borrow = if (bIn) 1 else 0
                val raw = a - b - borrow
                val expected = ((raw % 256) + 256) % 256   // 음수 mod 처리

                r.value shouldBe expected
                r.c shouldBe (raw >= 0)
                r.z shouldBe (r.value == 0)
                r.s shouldBe (r.value >= 128)

                val sA = if (a < 128) a else a - 256
                val sB = if (b < 128) b else b - 256
                val signedRaw = sA - sB - borrow
                val signedOverflow = signedRaw < -128 || signedRaw > 127
                r.v shouldBe signedOverflow
            }
        }
    }
}
```

음수 mod의 처리(`((raw % 256) + 256) % 256`)에 한 번 주의하자. Kotlin의 `%`는 결과의 부호가 좌변을 따르므로 `-1 % 256 == -1`이다. 우리가 원하는 것은 0~255 범위의 결과이므로 256을 더해 양수로 끌어올린 뒤 다시 mod한다. 이런 작은 함정 하나가 30분을 잡아먹는다. 미래의 자신을 위해 주석을 한 줄 박아두는 것도 좋다.

## "여기를 넘으면 절반은 끝났다"

휴, 길었다. 여기까지 따라온 독자에게 한 가지를 약속하고 싶다. **여기를 넘으면 8비트 CPU 짓기의 절반은 끝났다.** 정말이다.

이유는 단순하다. CPU의 동작 중에 가장 까다로운 부분이 산술과 플래그다. 메모리·버스·컨트롤러는 시간을 들이면 흐름이 보인다. 어셈블러는 패턴 매칭이다. 마이크로코드는 표 한 장이다. 그런데 **ADC/SBC의 V 플래그는 회로 차원의 진실과 추상적 의미가 어긋나는 거의 유일한 지점**이다. 이걸 손에 쥐어두면 나머지 명령어들은 다 비슷한 결로 처리된다.

게다가 우리는 단순히 "이해했다"가 아니라 **131,072 케이스의 자동 검증**까지 가진 상태다. 6502 emulator를 짠 수많은 사람이 "ADC를 손볼 때마다 식은땀을 흘렸다"고 하는데, 우리는 그럴 일이 없다. 코드를 고친 뒤 `./gradlew test` 한 번이면 모든 케이스가 다시 돈다. 빨간 줄이 안 보이면 자기 자신이 깨지 않았다는 확신을 얻는다.

이 확신이 정말 큰 무기다. 다음 챕터에서 메모리·버스·컨트롤러를 짤 때, ALU에 대한 불안 없이 작업할 수 있다. 그게 TDD가 가져다주는 마음의 평화다. ALU에 손을 댈 일이 생겨도 같은 안전망이 받쳐준다.

### 한 가지 더 — 진짜 emulator 개발자가 쓰는 표현

8비트 emulator 커뮤니티에서 자주 쓰는 표현 하나를 익혀두자. **"V 플래그는 거짓말한다."** 이건 농담 같지만, 자기 ALU가 잘못 동작할 때마다 자신에게 한숨처럼 내뱉는 말이다. "V 플래그가 또 거짓말해서 게임이 미궁으로 점프했다." 이 표현이 자기 입에서 나오기 시작하면, 자신이 emulator 개발자가 되어가는 중이라는 신호다. 즐기자.

> **GitHub 산출물**
>
> 이 챕터에서 추가될 GitHub 레포의 디렉터리는 다음과 같다.
>
> ```
> chapter-05/
>   build.gradle.kts        ← kotest 의존성 추가
>   src/main/kotlin/sap1/
>     AluResult.kt
>     Alu.kt                ← 5장 확장판: SF, OF 플래그 추가
>   src/test/kotlin/sap1/
>     AluAddTest.kt         ← 표 기반 (9개 행)
>     AluSubTest.kt         ← 표 기반 (7개 행)
>     AluPropertyTest.kt    ← property-based (5개 속성 × 1,000 케이스)
>     AluExhaustiveTest.kt  ← 전수조사 (ADD/SUB 각 131,072 단언)
> ```
>
> 실행:
> ```
> ./gradlew :chapter-05:test
> ```
>
> 총 검증 건수: 표 16건 + property 5,000건 + 전수조사 262,144건 ≈ **267,000건**. 한 번 실행에 약 1.5초.

## 마무리 — 무덤을 넘었다

다시 정리하자.

1. **2의 보수**가 "빼기를 더하기로" 만들어주는 마법을 손에 쥐었다
2. **C 플래그와 V 플래그**가 같은 ADD에서 서로 다른 거짓말을 추적한다는 사실을 봤다
3. **V 플래그 한 줄 공식** — `((A xor R) and (B xor R)) bit 7` — 을 익혔다
4. **SBC의 borrow 규약**(6502 관행)을 받아들였다
5. **kotest를 설치**하고 **표 기반 + property + 전수조사** 세 단계 테스트 전략을 도입했다
6. 131,072 × 2 = **262,144건의 자동 검증**으로 ALU의 안전망을 완성했다

이것이 우리의 ALU 챕터의 끝이다. 4장에서 짠 기본 가산기·감산기에 5장의 SF/OF가 얹혀 완성된 ALU가 손에 있다. 다음 챕터에서는 이 ALU와 3장의 PC·Clock, 그리고 새로 짤 메모리·버스·컨트롤러를 모두 연결해 **SAP-1이 처음으로 한 줄 프로그램을 실행하는 순간**을 만든다. "LDA 5; ADD 6; OUT; HLT"로 5 + 3 = 8을 출력하는, 16바이트 우주의 첫 햇빛이다.

그러니 잠깐 쉬어가자. 커피 한 잔 하면서 자기 V 플래그를 한 번 더 들여다보자. 너무 단순해서 거짓말하지 않을 것 같은 그 한 줄이 진짜로 모든 케이스에 옳다는 점이, 이상하게 위로가 된다. 6장에서 만나자.
