# 13장. 우리의 8비트 RISC를 설계하다

이 장을 시작하기 전에 한 가지를 인정하자. **ISA를 설계한다는 일은 무겁다.** 1970년대 IBM의 John Cocke는 801 프로젝트로 그것을 했다. 1980년대 초 Berkeley의 David Patterson은 RISC-I로 그것을 했고, 같은 시기 Stanford의 John Hennessy는 MIPS로 그것을 했다. 두 사람은 후일 튜링상을 받았다. 2010년대 들어 Krste Asanović와 같은 Berkeley의 연구자들이 RISC-V를 만들면서 그 무게는 다시 한 번 살아났다. ISA를 설계한다는 일은 컴퓨터 구조 분야가 한 사람에게 줄 수 있는 가장 큰 보상의 영역이다.

그런데 이제 우리가 그 일을 하려고 한다. 손에 든 도구는 Kotlin과 12주 동안 쌓아 올린 SAP-1·SAP-2 시뮬레이터 코드. 우리가 만들 ISA의 이름을 잠정적으로 부르자 — **RISC-8**. 8비트 데이터 폭에 RISC 정신을 얹은 합성 ISA. 이 장에서 우리는 RISC-8의 명령어 집합, 인코딩, 레지스터 구조, 인터럽트 처리까지 정면으로 결정한다. 그 결정을 ADR(Architecture Decision Record)로 적어 GitHub에 남긴다. **이 결정 하나하나가 책 전체의 가장 창의적인 산물이다.**

이 장은 거짓말처럼 무거워 보이지만, 정작 한 발씩 들여다보면 12장에서 이어받은 RISC 정신의 자연스러운 적용에 불과하다. Patterson과 Hennessy가 1980년대에 한 결정들을 우리가 8비트로 축소해서 다시 한 번 한다. 그 결정의 트레이드오프를 손에 익히는 일이 이 장의 진짜 보상이다. 같이 가 보자.

## 13.1 RISC 정신을 다시 펴 본다 — 다섯 가지 결정

12장에서 우리는 1980년대 RISC vs CISC 논쟁의 한 가운데로 갔다. Patterson과 Ditzel이 1980년에 발표한 한 줄을 다시 펴 보자.

> "Most programs made no use of the large variety of complex instructions."
>
> — Patterson, Berkeley RISC 결론 [웹-자료16]

복잡한 명령어가 거의 안 쓰인다는 발견. 그러면 복잡한 명령어를 빼고 단순한 명령어들로 채우자. 그 단순한 명령어들을 한 사이클에 끝내자. 그러면 IPC가 1에 가까워지고, 같은 시간에 더 많은 일을 한다.

이 정신이 다섯 가지 결정으로 정착했다. RISC 책마다 표현은 조금씩 다르지만 본질은 같다.

| 결정 | 내용 | 왜? |
|------|------|-----|
| **load/store 아키텍처** | 메모리 접근은 `LD`/`ST` 두 명령어만. 산술 연산은 레지스터끼리만. | 디코딩이 단순해진다. 한 명령어 안에 메모리 접근과 산술이 섞이지 않는다. |
| **고정 길이 명령어** | 모든 명령어가 같은 비트 길이 | fetch가 단순해진다. 파이프라인이 안정된다. |
| **단일 사이클 실행 목표** | IPC ≈ 1을 목표로 모든 명령어를 짠다 | 평균 throughput을 예측 가능하게 만든다. |
| **큰 레지스터 파일** | 16~32개의 범용 레지스터 | 메모리 접근 빈도를 줄인다. load/store 모델이 가능해진다. |
| **단순화된 어드레싱 모드** | 모드 가짓수를 5개 이하로 | 디코딩이 단순해진다. 컴파일러가 따라가기 쉬워진다. |

이 다섯 가지가 RISC의 골격이다. 32비트 RISC-V도, MIPS도, ARM의 32비트 모드도, 모두 이 골격 위에 살이 붙은 것이다. 우리가 짤 RISC-8도 같은 골격 위에 선다. 다만 한 가지 큰 차이가 있다 — **데이터 폭이 8비트다.** 32비트의 절반의 절반의 절반. 이 차이가 거의 모든 결정에 영향을 미친다.

## 13.2 8비트로 축소할 때의 트레이드오프

처음 떠오르는 생각은 단순하다 — "그러면 RISC-V를 그대로 8비트로 축소하면 되지 않을까?" 그런데 한 발 들여다보면 그게 그렇게 쉽지 않다.

RISC-V는 32비트 데이터 폭을 가정한다. 한 명령어가 32비트다. 32개의 32비트 레지스터가 있다. 메모리 주소가 32비트다(또는 64비트 변형도 있다). 이 모든 숫자를 4분의 1로 줄이면 어떻게 될까?

**8비트 명령어**. 첫 번째 함정이 여기서 등장한다. 256가지 패턴으로는 RISC가 필요로 하는 다양성을 표현할 수 없다. opcode 4비트만 떼어도 16개 명령어. 게다가 명령어 안에 레지스터 두세 개와 짧은 immediate 값까지 적어야 하는데, 8비트 안에 모두 들어갈 수가 없다. 정말 비좁다. 그래서 8비트 데이터 폭을 가진 칩들도 명령어는 보통 1~3바이트 가변 길이를 쓴다. 8080·Z80·8086 모두 그렇다. **그런데 가변 길이는 CISC의 친구다. RISC와는 어울리지 않는다.** 11장에서 8086 어셈블러가 3-pass였던 이유가 가변 길이 때문이었다는 점을 기억해두자.

여기서 한 가지 절충이 등장한다. **8비트 데이터 폭이지만 명령어는 16비트 고정 길이**로 가자. 데이터 패스는 여전히 한 사이클에 8비트를 다룬다. 그러나 명령어는 메모리에서 두 바이트씩 함께 fetch해서 디코딩한다. 8비트 데이터 폭 + 16비트 고정 명령어. 두 폭을 분리한 결정. 이게 RISC-8의 첫 번째 큰 결정이다.

> **결정 1: 16비트 고정 길이 명령어**
>
> 데이터는 8비트지만 명령어는 16비트 고정. 명령어 한 줄을 메모리에서 fetch할 때 두 바이트(연속 두 주소)를 함께 읽는다. 이 결정의 이유는 RISC의 "고정 길이" 원칙을 8비트에서도 살리기 위함이다. 단점은 메모리 효율(8비트 명령어보다 두 배 더 차지)이지만, 페다고지 우선의 단순함이 그 단점을 상쇄한다.

**두 번째 결정 — 레지스터 개수.** RISC-V는 32개, MIPS도 32개를 갖는다. 그런데 16비트 명령어 안에 레지스터 세 개를 적어야 한다고 해 보자. 32개의 레지스터는 5비트씩 적어야 한다. 5 × 3 = 15비트. 16비트 명령어 안에 opcode를 위한 자리가 1비트밖에 남지 않는다. 이건 안 된다. 정말 답답한 상황이다.

그래서 우리는 **16개 레지스터**로 간다. 4비트씩 세 개 = 12비트. opcode를 위한 4비트가 남는다. 16개 opcode가 충분한가? Berkeley RISC-I이 32개 명령어를 가졌고, MIPS subset도 비슷한 수준이라는 점을 기억하면, 우리가 짤 8비트 RISC-8에 16개 + 약간의 확장 opcode면 충분하다. 16개로 가자.

> **결정 2: 16개 범용 레지스터 R0~R15**
>
> 32개를 갖고 싶지만 16비트 명령어 안에 들어가지 않는다. RISC-V의 RV32E(임베디드 변형)도 같은 이유로 16 레지스터로 축소된 사례가 있다. RISC-8은 R0~R15를 갖는다. R0은 항상 0(읽기 전용)으로 약속한다 — 이건 MIPS의 $0와 같은 트릭이다. R15는 link register(JAL의 반환 주소 저장)로 약속한다 — 이건 ARM의 LR와 같은 트릭이다. 13개 + R0(zero) + R15(LR) + R14(SP) 정도의 분포로 정착시킨다.

**세 번째 결정 — load/store.** RISC의 핵심 원칙. SAP-2에서는 `ADD addr` 같은 명령어가 메모리에서 직접 값을 읽어 A에 더했다. RISC-8에서는 그게 두 명령어로 분리된다 — `LD R1, [R2]`로 메모리에서 R1으로 적재한 다음, `ADD R3, R3, R1`로 R3에 R1을 더한다. 한 명령어가 두 명령어가 되는 셈이다. 정말 번거롭다고 느낄 수 있지만, 이게 RISC의 정신이다. **메모리 접근과 산술을 섞지 않으면 디코딩이 단순해진다.**

> **결정 3: load/store 아키텍처**
>
> 메모리 접근은 `LD Rd, [Rs+imm]`과 `ST Rs, [Rd+imm]` 두 명령어로만. 산술·논리 연산은 레지스터 사이에서만. 코드가 길어지지만 디코딩과 파이프라인이 깨끗해진다. RISC 정신 그대로.

**네 번째 결정 — 어드레싱 모드.** RISC-V는 `imm(rs1)` 한 가지 모드만 갖는다. 8086은 17가지 모드를 갖는다. 우리는 어디쯤에 설까? 단순함의 정신에 따라 **두 가지**로 간다 — `[Rs]`(레지스터 간접), `[Rs+imm]`(레지스터 + 4비트 짧은 오프셋). 그 외의 모드(zero page, indirect, indexed indirect 같은 6502식의 화려한 모드들)는 빼자. 단순함이 미덕이다.

> **결정 4: 두 가지 어드레싱 모드만**
>
> `[Rs]`와 `[Rs+imm4]`. 그게 전부다. 컴파일러가 더 복잡한 어드레싱을 짜고 싶으면 명령어 두 줄로 풀어내면 된다. Berkeley RISC-I의 정신.

**다섯 번째 결정 — 단일 사이클 vs 다중 사이클.** RISC는 단일 사이클을 목표한다. 그런데 우리가 짤 RISC-8은 시뮬레이터이지 실제 하드웨어가 아니다. 한 명령어 안에 fetch + decode + execute의 모든 일이 한 함수 호출에 들어간다. 시뮬레이터 레벨에서는 그저 "한 명령어 = 한 step"이다. 다만 14장(cycle-accurate)에서 같은 RISC-8을 사이클 단위로 다시 짤 때 IPC ≈ 1 약속이 직접 검증될 것이다. 지금 단계에서는 "instruction-accurate" 약속만 하자.

> **결정 5: 시뮬레이터는 instruction-accurate**
>
> 한 명령어가 한 step이다. 14장에서 같은 RISC-8을 cycle-accurate로 리팩토링한다. 그때 IPC ≈ 1을 손으로 검증한다.

자, 다섯 가지 결정이 끝났다. 16비트 고정 길이 명령어, 16개 범용 레지스터, load/store, 두 가지 어드레싱 모드, instruction-accurate. 이게 RISC-8의 골격이다.

## 13.3 명령어 인코딩 — 16비트의 풍경

이제 16비트 안에 무엇을 어떻게 적을지를 결정하자. RISC 명령어 인코딩은 보통 세 가지 형식으로 나뉜다 — **R-type**, **I-type**, **J-type**. 이건 MIPS의 분류로, RISC-V도 본질적으로 같은 골격을 따른다. 우리도 그대로 따라가자.

**R-type — 레지스터 세 개를 쓰는 명령어 (산술·논리)**

```
 bit:  15  14  13  12  11  10   9   8   7   6   5   4   3   2   1   0
      ┌───────────────┬──────────────┬──────────────┬──────────────┐
      │   opcode (4)  │   Rd (4)     │   Rs1 (4)    │   Rs2 (4)    │
      └───────────────┴──────────────┴──────────────┴──────────────┘
```

예를 들어 `ADD R3, R1, R2`(R3 = R1 + R2)는 opcode = `0001`(ADD), Rd = `0011`(R3), Rs1 = `0001`(R1), Rs2 = `0010`(R2). 16비트로 `0001 0011 0001 0010` = `0x1312`.

**I-type — 레지스터 두 개 + 4비트 immediate (load/store/짧은 점프/즉치 산술)**

```
 bit:  15  14  13  12  11  10   9   8   7   6   5   4   3   2   1   0
      ┌───────────────┬──────────────┬──────────────┬──────────────┐
      │   opcode (4)  │   Rd (4)     │   Rs1 (4)    │   imm4 (4)   │
      └───────────────┴──────────────┴──────────────┴──────────────┘
```

예를 들어 `LD R3, [R1+5]`는 opcode = `0100`(LD), Rd = R3, Rs1 = R1, imm4 = `0101`(5). 4비트 immediate는 -8부터 +7까지(또는 0부터 15까지) 표현한다. 데이터 폭이 8비트라 4비트면 절반의 풍경을 다룰 수 있다. 더 큰 값을 다룰 때는 `LI Rd, imm8` 같은 별도 명령어를 두 번 호출해서 8비트 immediate를 두 4비트로 나눠 적재한다.

**J-type — 큰 점프 명령어**

```
 bit:  15  14  13  12  11  10   9   8   7   6   5   4   3   2   1   0
      ┌───────────────┬──────────────────────────────────────────────┐
      │   opcode (4)  │              addr12 (12)                      │
      └───────────────┴──────────────────────────────────────────────┘
```

12비트 주소면 4096 위치까지 점프할 수 있다. 8비트 데이터 폭의 칩치고 충분한 범위. 더 멀리 점프해야 하면 R-type의 `JR Rd`(레지스터 간접 점프)를 쓰면 된다.

명령어 인코딩 표를 한 번 펴 보자.

| Mnemonic | Format | opcode | 동작 |
|----------|--------|--------|------|
| `NOP` | R | `0000` | 아무 일도 안 함 |
| `ADD Rd, Rs1, Rs2` | R | `0001` | Rd = (Rs1 + Rs2) & 0xFF |
| `SUB Rd, Rs1, Rs2` | R | `0010` | Rd = (Rs1 - Rs2) & 0xFF |
| `AND Rd, Rs1, Rs2` | R | `0011` | Rd = Rs1 & Rs2 |
| `OR Rd, Rs1, Rs2` | R | `0100` | Rd = Rs1 \| Rs2 |
| `XOR Rd, Rs1, Rs2` | R | `0101` | Rd = Rs1 ^ Rs2 |
| `SHL Rd, Rs1, Rs2` | R | `0110` | Rd = Rs1 << (Rs2 & 7) |
| `SHR Rd, Rs1, Rs2` | R | `0111` | Rd = Rs1 >> (Rs2 & 7) (논리) |
| `LD Rd, [Rs1+imm4]` | I | `1000` | Rd = MEM[Rs1 + imm4] |
| `ST Rs1, [Rd+imm4]` | I | `1001` | MEM[Rd + imm4] = Rs1 |
| `LI Rd, imm4` | I | `1010` | Rd = sign_extend(imm4) |
| `ADDI Rd, Rs1, imm4` | I | `1011` | Rd = (Rs1 + imm4) & 0xFF |
| `BEQ Rs1, Rs2, imm4` | I | `1100` | if Rs1 == Rs2: PC += imm4 |
| `BNE Rs1, Rs2, imm4` | I | `1101` | if Rs1 != Rs2: PC += imm4 |
| `JAL addr12` | J | `1110` | R15 = PC + 2; PC = addr12 |
| `JR Rd` | R | `1111` | PC = Rd (R-type 안에서 Rs1=Rs2=0) |

16개 명령어. RISC 정신의 가장 단순한 형태. **이게 RISC-8의 ISA 전체**다.

생각보다 단출하지 않은가? 32비트 RISC-V도 RV32I subset이 47개 명령어다. 우리 16개는 그 절반이 안 된다. 그런데 이 16개로 8비트 시대의 거의 모든 일을 표현할 수 있다. **단순함의 미덕이 여기에 있다.** 단순한 도구로 큰일을 한다.

> **사이드바: Berkeley RISC-I의 32개 명령어**
>
> 1981년 David Patterson과 그의 학생들이 만든 Berkeley RISC-I는 32개 명령어를 가진 32비트 RISC였다. 44,420개 트랜지스터로 구현됐다. 같은 시기 Intel 8086은 29,000개 트랜지스터에 117개 base 명령어를 가졌다. **트랜지스터 수는 비슷한데 명령어 수는 4배가 적다.** 그러면 어디에 그 트랜지스터를 썼느냐? 32개 레지스터의 큰 파일과 단일 사이클 실행을 위한 회로에 썼다. "복잡함을 명령어에 쏟지 말고 레지스터와 파이프라인에 쏟아라." 이 한 줄이 1980년대 RISC의 본질이었다. 우리 RISC-8의 16개 명령어는 그 정신을 8비트로 축소한 결과다.

## 13.4 Kotlin sealed class로 ISA 모델링

ISA를 코드로 옮기자. 7장에서 SAP-1의 명령어를 sealed class로 모델링한 그 패턴이 RISC-8에도 그대로 쓰인다. 다만 더 풍부한 형태로 발전한다.

```kotlin
sealed class Instruction {
    abstract val opcode: Int
    abstract fun encode(): Int   // 16비트 정수로

    // R-type
    data class Nop(val raw: Int = 0) : Instruction() {
        override val opcode = 0x0
        override fun encode() = 0x0000
    }

    data class Add(val rd: Int, val rs1: Int, val rs2: Int) : Instruction() {
        override val opcode = 0x1
        override fun encode() =
            (opcode shl 12) or (rd shl 8) or (rs1 shl 4) or rs2
    }

    data class Sub(val rd: Int, val rs1: Int, val rs2: Int) : Instruction() {
        override val opcode = 0x2
        override fun encode() =
            (opcode shl 12) or (rd shl 8) or (rs1 shl 4) or rs2
    }

    // ... AND, OR, XOR, SHL, SHR (모두 같은 R-type 인코딩)

    // I-type
    data class Ld(val rd: Int, val rs1: Int, val imm4: Int) : Instruction() {
        override val opcode = 0x8
        override fun encode() =
            (opcode shl 12) or (rd shl 8) or (rs1 shl 4) or (imm4 and 0xF)
    }

    data class St(val rs1: Int, val rd: Int, val imm4: Int) : Instruction() {
        override val opcode = 0x9
        override fun encode() =
            (opcode shl 12) or (rd shl 8) or (rs1 shl 4) or (imm4 and 0xF)
    }

    data class Li(val rd: Int, val imm4: Int) : Instruction() {
        override val opcode = 0xA
        override fun encode() =
            (opcode shl 12) or (rd shl 8) or (imm4 and 0xF)
    }

    data class Addi(val rd: Int, val rs1: Int, val imm4: Int) : Instruction() {
        override val opcode = 0xB
        override fun encode() =
            (opcode shl 12) or (rd shl 8) or (rs1 shl 4) or (imm4 and 0xF)
    }

    data class Beq(val rs1: Int, val rs2: Int, val imm4: Int) : Instruction() {
        override val opcode = 0xC
        override fun encode() =
            (opcode shl 12) or (rs1 shl 8) or (rs2 shl 4) or (imm4 and 0xF)
    }

    data class Bne(val rs1: Int, val rs2: Int, val imm4: Int) : Instruction() {
        override val opcode = 0xD
        override fun encode() =
            (opcode shl 12) or (rs1 shl 8) or (rs2 shl 4) or (imm4 and 0xF)
    }

    // J-type
    data class Jal(val addr12: Int) : Instruction() {
        override val opcode = 0xE
        override fun encode() =
            (opcode shl 12) or (addr12 and 0xFFF)
    }

    // R-type 변형
    data class Jr(val rd: Int) : Instruction() {
        override val opcode = 0xF
        override fun encode() =
            (opcode shl 12) or (rd shl 8)
    }
}
```

이 정도다. sealed class 한 묶음으로 16개 명령어가 모두 표현된다. 7장의 SAP-1 명령어와 같은 패턴인데 더 풍부하다. 각 명령어가 자기 인코딩을 안다. 디코더는 그저 역과정으로 돌리면 된다.

```kotlin
object Decoder {
    fun decode(raw: Int): Instruction {
        val opcode = (raw shr 12) and 0xF
        val rd = (raw shr 8) and 0xF
        val rs1 = (raw shr 4) and 0xF
        val rs2 = raw and 0xF
        val imm4 = raw and 0xF
        val addr12 = raw and 0xFFF

        return when (opcode) {
            0x0 -> Instruction.Nop()
            0x1 -> Instruction.Add(rd, rs1, rs2)
            0x2 -> Instruction.Sub(rd, rs1, rs2)
            0x3 -> Instruction.And(rd, rs1, rs2)
            0x4 -> Instruction.Or(rd, rs1, rs2)
            0x5 -> Instruction.Xor(rd, rs1, rs2)
            0x6 -> Instruction.Shl(rd, rs1, rs2)
            0x7 -> Instruction.Shr(rd, rs1, rs2)
            0x8 -> Instruction.Ld(rd, rs1, imm4)
            0x9 -> Instruction.St(rs1, rd, imm4)
            0xA -> Instruction.Li(rd, imm4)
            0xB -> Instruction.Addi(rd, rs1, imm4)
            0xC -> Instruction.Beq(rs1, rs2, imm4)
            0xD -> Instruction.Bne(rs1, rs2, imm4)
            0xE -> Instruction.Jal(addr12)
            0xF -> Instruction.Jr(rd)
            else -> error("unreachable")
        }
    }
}
```

디코더가 단 한 줄짜리 `when` 표현식이다. **고정 길이 명령어의 미덕이 여기서 빛을 발한다.** 16비트를 한 묶음으로 fetch하고, 한 번의 `when`으로 디코딩한다. SAP-2의 가변 길이 디코딩에서 우리가 겪은 그 번거로움이 RISC-8에는 없다. 정말 깔끔하다.

## 13.5 CPU 본체 — execute의 한 함수

ISA가 정해졌으니 CPU 본체를 짜자. 9장에서 짠 SAP-2 CPU의 구조를 거의 그대로 가져오되, 단일 누산기 A 대신 16개 레지스터 배열로 바뀐다.

```kotlin
class Risc8Cpu(val memory: IntArray = IntArray(256)) {
    val registers = IntArray(16)       // R0~R15, 모두 8비트
    var pc: Int = 0                    // PC는 12비트지만 Int로 다룬다
    var halted: Boolean = false

    // 플래그: RISC는 보통 명시적 플래그를 안 갖지만,
    // 우리는 디버깅 편의를 위해 마지막 ALU 결과의 Z/C를 캐싱한다.
    var zero: Boolean = false
    var carry: Boolean = false

    fun stepInstruction() {
        if (halted) return

        // fetch: 두 바이트 = 하나의 16비트 명령어
        val raw = (memory[pc] and 0xFF) shl 8 or (memory[pc + 1] and 0xFF)
        pc += 2

        // decode
        val instr = Decoder.decode(raw)

        // execute
        execute(instr)

        // R0은 항상 0으로 강제
        registers[0] = 0
    }

    private fun execute(instr: Instruction) {
        when (instr) {
            is Instruction.Nop -> { /* 아무것도 안 함 */ }

            is Instruction.Add -> {
                val sum = registers[instr.rs1] + registers[instr.rs2]
                registers[instr.rd] = sum and 0xFF
                carry = sum > 0xFF
                zero = registers[instr.rd] == 0
            }

            is Instruction.Sub -> {
                val diff = registers[instr.rs1] - registers[instr.rs2]
                registers[instr.rd] = diff and 0xFF
                carry = diff >= 0
                zero = registers[instr.rd] == 0
            }

            is Instruction.And -> {
                registers[instr.rd] = registers[instr.rs1] and registers[instr.rs2]
                zero = registers[instr.rd] == 0
            }

            is Instruction.Or -> {
                registers[instr.rd] = registers[instr.rs1] or registers[instr.rs2]
                zero = registers[instr.rd] == 0
            }

            is Instruction.Xor -> {
                registers[instr.rd] = registers[instr.rs1] xor registers[instr.rs2]
                zero = registers[instr.rd] == 0
            }

            is Instruction.Shl -> {
                val n = registers[instr.rs2] and 0x7
                registers[instr.rd] = (registers[instr.rs1] shl n) and 0xFF
                zero = registers[instr.rd] == 0
            }

            is Instruction.Shr -> {
                val n = registers[instr.rs2] and 0x7
                registers[instr.rd] = (registers[instr.rs1] and 0xFF) shr n
                zero = registers[instr.rd] == 0
            }

            is Instruction.Ld -> {
                val addr = (registers[instr.rs1] + instr.imm4) and 0xFF
                registers[instr.rd] = memory[addr] and 0xFF
            }

            is Instruction.St -> {
                val addr = (registers[instr.rd] + instr.imm4) and 0xFF
                memory[addr] = registers[instr.rs1] and 0xFF
            }

            is Instruction.Li -> {
                val signExtended = if (instr.imm4 and 0x8 != 0) {
                    instr.imm4 or 0xF0
                } else {
                    instr.imm4
                }
                registers[instr.rd] = signExtended and 0xFF
            }

            is Instruction.Addi -> {
                val sum = registers[instr.rs1] + instr.imm4
                registers[instr.rd] = sum and 0xFF
                carry = sum > 0xFF
                zero = registers[instr.rd] == 0
            }

            is Instruction.Beq -> {
                if (registers[instr.rs1] == registers[instr.rs2]) {
                    pc += signExtend4(instr.imm4) * 2   // 명령어 단위 오프셋
                }
            }

            is Instruction.Bne -> {
                if (registers[instr.rs1] != registers[instr.rs2]) {
                    pc += signExtend4(instr.imm4) * 2
                }
            }

            is Instruction.Jal -> {
                registers[15] = pc and 0xFF             // 반환 주소 저장 (8비트 잘림)
                pc = instr.addr12
            }

            is Instruction.Jr -> {
                pc = registers[instr.rd]
            }
        }
    }

    private fun signExtend4(imm4: Int): Int =
        if (imm4 and 0x8 != 0) imm4 or 0xFFFFFFF0.toInt() else imm4

    fun run(maxSteps: Int = 100_000) {
        var steps = 0
        while (!halted && steps < maxSteps) {
            stepInstruction()
            steps++
        }
    }
}
```

이 한 클래스가 RISC-8 CPU의 전부다. **150줄 정도.** SAP-2의 명령어 39개를 옮긴 코드에 비해 훨씬 짧다. 16개 명령어를 한 묶음의 `when`에 적은 결과가 이 정도다. 이게 RISC의 가독성이다 — 명령어 수가 적고 모두 같은 형식으로 동작하니까 코드가 한 그림으로 보인다.

테스트도 함께 짜자.

```kotlin
class Risc8CpuTest : FunSpec({
    test("LI는 4비트 immediate를 sign-extend해서 레지스터에 적재한다") {
        val cpu = Risc8Cpu()
        // LI R1, 5 = 0xA105
        cpu.memory[0] = 0xA1; cpu.memory[1] = 0x05
        cpu.stepInstruction()
        cpu.registers[1] shouldBe 5
    }

    test("ADD R3, R1, R2 = R1 + R2") {
        val cpu = Risc8Cpu()
        cpu.registers[1] = 3
        cpu.registers[2] = 5
        // ADD R3, R1, R2 = 0x1312
        cpu.memory[0] = 0x13; cpu.memory[1] = 0x12
        cpu.stepInstruction()
        cpu.registers[3] shouldBe 8
        cpu.zero shouldBe false
    }

    test("R0은 항상 0이다 — 어떤 명령어도 R0에 값을 쓰지 못한다") {
        val cpu = Risc8Cpu()
        // LI R0, 7 (R0에 7을 적재 시도)
        cpu.memory[0] = 0xA0; cpu.memory[1] = 0x07
        cpu.stepInstruction()
        cpu.registers[0] shouldBe 0   // 명령어 실행 직후 강제로 0이 된다
    }

    test("BEQ가 같으면 점프한다") {
        val cpu = Risc8Cpu()
        cpu.registers[1] = 5
        cpu.registers[2] = 5
        // BEQ R1, R2, 2 = 0xC122 (PC += 2 instructions = 4 bytes)
        cpu.memory[0] = 0xC1; cpu.memory[1] = 0x22
        cpu.stepInstruction()
        cpu.pc shouldBe 2 + 4   // 다음 명령어 위치(2) + 점프 오프셋(4)
    }

    test("JAL은 R15에 반환 주소를 저장한다") {
        val cpu = Risc8Cpu()
        // JAL 0x100 = 0xE100
        cpu.memory[0] = 0xE1; cpu.memory[1] = 0x00
        cpu.stepInstruction()
        cpu.pc shouldBe 0x100
        cpu.registers[15] shouldBe 2   // 다음 명령어 위치
    }
})
```

다섯 테스트가 RISC-8의 핵심 동작을 잡는다. 더 큰 회귀 셋은 10장의 테스트 ROM 패턴을 그대로 적용해서 각 명령어를 짧은 프로그램으로 검증한다. 30~40개 테스트가 들어간다.

## 13.6 인터럽트의 RISC다운 단순화

여기서 어려운 결정 하나가 남아 있다. **인터럽트.**

전통적 8비트 CISC는 인터럽트가 복잡했다. Z80은 IM 0, IM 1, IM 2의 세 가지 모드를 가졌다. 8086은 256개 인터럽트 벡터 테이블을 IVT(Interrupt Vector Table)로 갖고 있었다. 6502는 NMI, IRQ, BRK의 세 가지를 별도 벡터로 받았다. CISC다운 화려한 메커니즘들.

RISC는 어떻게 했을까? **단순함**으로 갔다. 가장 영향력 있는 RISC ISA인 RISC-V는 **trap**이라는 한 가지 메커니즘으로 인터럽트와 예외를 모두 통합한다.

- trap이 발생하면 PC를 미리 정해둔 단일 trap vector(`mtvec`)로 점프한다.
- 어떤 trap이었는지는 별도 cause register(`mcause`)에 기록된다.
- 핸들러는 cause register를 읽어 무슨 trap인지 분기한다.

화려한 IVT 대신 **한 vector + 한 cause register**. 이 한 줄이 RISC의 정신을 정확히 보여 준다 — "하드웨어가 256개 vector를 다 외울 필요 없다. 소프트웨어가 cause register를 보고 분기하면 된다." 복잡함을 하드웨어가 아니라 소프트웨어에 둔다. **이게 RISC가 1980년대에 한 가장 깊은 결정 중 하나다.**

우리 RISC-8도 같은 길로 가자.

> **결정 6: 단일 trap vector + cause register**
>
> 인터럽트가 발생하면 PC가 trap vector 주소(예: 0x80, 고정)로 점프한다. 인터럽트 발생 직전의 PC는 R14(또는 별도 epc 레지스터)에 저장된다. 어떤 인터럽트였는지는 `cause` 레지스터(별도)에 기록된다. 핸들러는 cause를 읽어 `BEQ cause, R1, handle_timer` 식으로 분기한다.

코드로 옮기면 이렇다.

```kotlin
class Risc8Cpu(/* ... */) {
    // 기존 registers, pc, halted 외에 추가
    var cause: Int = 0
    var epc: Int = 0
    var interruptsEnabled: Boolean = false
    private val pendingInterrupts = mutableListOf<Int>()  // 큐

    companion object {
        const val TRAP_VECTOR = 0x80   // 고정 trap vector 주소
    }

    fun requestInterrupt(causeCode: Int) {
        pendingInterrupts += causeCode
    }

    fun stepInstruction() {
        if (halted) return

        // 매 명령어 시작에서 인터럽트 체크
        if (interruptsEnabled && pendingInterrupts.isNotEmpty()) {
            val causeCode = pendingInterrupts.removeAt(0)
            epc = pc
            cause = causeCode
            pc = TRAP_VECTOR
            interruptsEnabled = false   // nested trap 방지
        }

        // 이하 기존과 동일
        val raw = (memory[pc] and 0xFF) shl 8 or (memory[pc + 1] and 0xFF)
        pc += 2
        val instr = Decoder.decode(raw)
        execute(instr)
        registers[0] = 0
    }

    // trap 처리 후 핸들러가 호출할 명령어
    // 실제로는 어셈블리 레벨에서 별도 명령어(RETT 같은)로 표현하는 게 RISC답지만,
    // 우리 단순화 버전은 직접 메서드로 노출
    fun returnFromTrap() {
        pc = epc
        interruptsEnabled = true
    }
}
```

인터럽트의 본질이 30줄 안에 들어간다. **RISC의 단순함이 만든 가독성이다.** Z80의 IM 2 처리 코드와 비교해보면 차이가 극명하다 — Z80 emulator의 인터럽트 처리는 보통 100줄을 넘는다. 같은 일을 RISC는 30줄로 한다. 단순함이 자기 의미를 정확히 한다.

> **사이드바: ARM의 인터럽트도 RISC답게 단순**
>
> ARM Cortex-M은 NVIC(Nested Vectored Interrupt Controller)를 갖지만, ISA 레벨에서는 우리 RISC-8과 비슷한 구조다. trap이 발생하면 정해진 vector table 주소로 점프하고, 어떤 trap이었는지는 별도 IPSR(Interrupt Program Status Register)에 적힌다. 8086 IVT의 256 벡터를 외우는 대신, ARM은 vector table을 메모리에 한 묶음으로 두고 cause를 별도 레지스터로 분리한다. 1986년 ARM 설계자들이 한 결정이 우리 RISC-8 결정과 같은 결이다. RISC 정신이 어떻게 이어졌는지를 보여 주는 한 사례다.

## 13.7 Fibonacci를 RISC-8 어셈블리로 — 4가지 ISA와의 비교

11장에서 우리는 같은 Fibonacci 알고리즘을 8080·6502·Z80·8086의 네 가지 어셈블리로 비교해 봤다. 이제 다섯 번째 — **RISC-8** — 을 그 비교 표에 한 줄 추가하자. 이게 이 장의 정서적 절정이다.

먼저 Fibonacci 시퀀스의 10번째 수를 계산하는 RISC-8 어셈블리.

```asm
; Fibonacci(n) — n번째 피보나치 수를 R1에 둔다
; R3 = n (몇 번째까지 계산할지, 여기서는 10)
; R1 = fib(n)에 들어갈 결과
; R2 = 직전 항 (fib[k-1])

start:
        LI   R3, 10        ; n = 10
        LI   R1, 1         ; fib[1] = 1
        LI   R2, 0         ; fib[0] = 0
        LI   R4, 1         ; 카운터 시작 = 1 (fib[1]까지는 이미 계산됨)

loop:
        BEQ  R3, R4, done  ; R3 == R4면 끝
        ADD  R5, R1, R2    ; R5 = fib[k-1] + fib[k]
        ADD  R2, R1, R0    ; R2 = R1 (R0이 0이라 ADD가 MOV처럼)
        ADD  R1, R5, R0    ; R1 = R5
        ADDI R4, R4, 1     ; counter++
        JR   R6_unused     ; (단순화: BNE 또는 JAL loop으로 점프하는 게 정직.
                           ;  여기서는 BNE R4, R3, -5 같은 직전 BEQ의 반대)

done:
        ST   R1, [R0+0]    ; 메모리 주소 0에 결과 저장
        ; HLT
```

(주의: 위 코드는 ISA의 사용법을 보여 주는 의사 어셈블리에 가깝다. 실제 작동시키려면 BNE 처리를 정확히 적어야 한다. 13.8절의 어셈블러가 다음 단계에서 이를 다듬는다.)

이걸 11장의 표와 함께 정리해보자.

| ISA | Fibonacci 코드 라인 수 | 사용한 레지스터 | 특이점 |
|-----|------------------------|------------------|--------|
| Intel 8080 | ~12줄 | A, B, C, HL | `MOV` + `ADD` 분리 |
| MOS 6502 | ~10줄 (zero page 사용) | A, X, page-0 메모리 | zero page가 레지스터 역할 |
| Zilog Z80 | ~10줄 | A, B, C, HL, alt 레지스터 | 더 풍부한 명령어 |
| Intel 8086 | ~8줄 | AX, BX, CX, DX | 16비트 + 더 표현력 있는 어셈블리 |
| **RISC-8 (우리)** | **~10줄** | **R1, R2, R3, R4, R5** | **모두 같은 격의 레지스터, load/store 분리** |

라인 수만 보면 RISC-8이 8086보다 길고 8080과 비슷하다. 그런데 한 가지 흥미로운 점이 있다. **RISC-8의 한 줄, 한 줄이 모두 같은 비용으로 실행된다.** 8086의 `MOV AX, [BX+SI+disp]` 같은 한 줄은 사실 메모리 접근 + 인덱싱 + 적재의 세 가지 일을 한 명령어에 욱여넣은 것이다. 그 한 줄이 4~5사이클이 걸린다. RISC-8의 두 줄(LD + 별도 산술)은 각각 1사이클씩 = 2사이클이다. **라인 수는 많지만 사이클 수는 더 적다.**

이 점이 1980년대 RISC가 CISC를 이긴 진짜 이유다 — **한 명령어가 짧은 시간에 끝나면 평균 throughput이 늘어난다.** 우리가 짤 RISC-8 cycle-accurate 시뮬레이터(14장)에서 이 사실을 손에 직접 잡을 것이다. 라인 수의 가독성과 사이클 수의 효율이 서로 다른 차원의 미덕이라는 점이 13장의 깊은 깨달음이다.

> **사이드바: MIPS의 delay slot — RISC가 컴파일러에 책임을 떠넘긴 사례**
>
> Stanford MIPS는 RISC 정신의 극단을 갔다. **delay slot**이라는 매우 유명한 결정 — 점프 명령어 바로 다음 한 줄은 점프 여부와 무관하게 실행된다. 이건 파이프라인을 단순하게 만들기 위해 하드웨어가 의도적으로 갖춘 함정이다. 그 함정을 메우는 책임은 컴파일러에게 떠넘긴다. 컴파일러가 점프 뒤에 안전하게 실행될 수 있는 한 줄을 골라 넣어야 한다. "복잡함을 하드웨어가 아니라 소프트웨어에 둔다"라는 RISC 정신의 가장 극단적 사례. RISC-V는 delay slot을 빼서 더 깔끔해졌지만, MIPS의 결정은 RISC가 어디까지 갈 수 있는지를 보여 주는 학습 사례다. 우리 RISC-8은 delay slot을 도입하지 않는다 — 페다고지 단순함이 우선이다.

## 13.8 RISC-8 어셈블러

7장의 SAP-1 어셈블러 패턴이 RISC-8에도 그대로 적용된다. 다만 명령어 인코딩이 16비트라 출력은 2바이트씩이다. 짧게 짚자.

```kotlin
class Risc8Assembler {
    fun assemble(source: String): ByteArray {
        val tokens = Lexer(source).tokenize()
        val symbolTable = buildSymbolTable(tokens)
        return generateBytes(tokens, symbolTable)
    }

    private fun parseInstruction(parts: List<String>, symbolTable: Map<String, Int>): Instruction {
        val mnemonic = parts[0].uppercase()
        return when (mnemonic) {
            "NOP" -> Instruction.Nop()
            "ADD" -> Instruction.Add(parseReg(parts[1]), parseReg(parts[2]), parseReg(parts[3]))
            "SUB" -> Instruction.Sub(parseReg(parts[1]), parseReg(parts[2]), parseReg(parts[3]))
            "AND" -> Instruction.And(parseReg(parts[1]), parseReg(parts[2]), parseReg(parts[3]))
            "OR"  -> Instruction.Or (parseReg(parts[1]), parseReg(parts[2]), parseReg(parts[3]))
            "XOR" -> Instruction.Xor(parseReg(parts[1]), parseReg(parts[2]), parseReg(parts[3]))
            "SHL" -> Instruction.Shl(parseReg(parts[1]), parseReg(parts[2]), parseReg(parts[3]))
            "SHR" -> Instruction.Shr(parseReg(parts[1]), parseReg(parts[2]), parseReg(parts[3]))
            "LI"  -> Instruction.Li (parseReg(parts[1]), parseImm(parts[2]))
            "ADDI" -> Instruction.Addi(parseReg(parts[1]), parseReg(parts[2]), parseImm(parts[3]))
            "BEQ" -> Instruction.Beq(parseReg(parts[1]), parseReg(parts[2]), parseRelImm(parts[3], symbolTable))
            "BNE" -> Instruction.Bne(parseReg(parts[1]), parseReg(parts[2]), parseRelImm(parts[3], symbolTable))
            "JAL" -> Instruction.Jal(parseAddr(parts[1], symbolTable))
            "JR"  -> Instruction.Jr(parseReg(parts[1]))
            // LD/ST는 "LD R1, [R2+5]" 형식 파싱이 더 복잡 — 별도 함수
            else -> error("unknown mnemonic: $mnemonic")
        }
    }

    private fun parseReg(s: String): Int =
        s.removePrefix("R").toInt()

    // ... 나머지 도우미 함수
}
```

7장 어셈블러와 본질적으로 같은 골격이다. sealed class에 한 가지를 추가하고, parser에 한 줄을 추가한다. 이미 익숙한 패턴이 우리 손에서 자기 변주를 만들어낸다. **익숙한 도구의 응용**이 학습 곡선의 가장 큰 보상이다.

## 13.9 ADR — 결정의 기록을 남기자

이 장에서 우리가 내린 결정들을 ADR(Architecture Decision Record)로 GitHub에 남기자. ADR은 소프트웨어 아키텍처 분야에서 "왜 이 결정을 내렸는가"를 기록하는 표준 양식이다. 우리도 같은 양식으로 남긴다.

```markdown
# ADR-001: 16비트 고정 길이 명령어
- Status: Accepted (2026-05-13)
- Context: 8비트 데이터 폭. 256가지 패턴으로는 RISC가 필요로 하는
  명령어 다양성을 표현할 수 없음. 가변 길이는 CISC와 어울림.
- Decision: 16비트 고정 길이. 두 바이트씩 fetch.
- Consequences:
  - (+) 디코딩이 한 번의 when으로 떨어진다.
  - (+) 파이프라인 친화적 (14장에서 cycle-accurate로 검증).
  - (-) 메모리 효율이 8비트 명령어 대비 50%.

# ADR-002: 16개 범용 레지스터 R0~R15
- ... (이하 같은 양식)
```

여섯 개 ADR(결정 1~6)을 모두 적어두면, 후일 RISC-8을 확장하거나 재해석하는 사람이 "왜 그렇게 결정했는가"를 손에 쥘 수 있다. **결정을 남긴다는 것은 결정을 더 신중하게 한다는 뜻**이기도 하다. ISA 설계의 책임을 자기 손으로 한 번 느껴 보자.

## 13.10 한 챕터를 마치며 — 4부의 정서적 절정

이 장에서 우리가 손에 쥔 것을 정리해보자.

첫째, **ISA를 설계한다는 일이 무엇인지** 손에 잡혔다. Patterson과 Hennessy가 1980년대에 한 결정들의 작은 변주를 우리도 한 번 했다. 16비트 고정 길이, 16개 레지스터, load/store, 두 가지 어드레싱 모드, instruction-accurate. 다섯 가지 결정 + 인터럽트 한 가지가 RISC-8의 골격이다.

둘째, **명령어 16개로 8비트 RISC를 표현했다.** R-type, I-type, J-type의 세 가지 인코딩이 16비트 안에 깔끔하게 들어간다. sealed class와 `when` 디스패치로 Kotlin에서 그대로 옮긴다. 코드가 150줄이다. SAP-2의 39개 명령어를 옮긴 코드의 절반 수준.

셋째, **인터럽트를 RISC답게 단순화했다.** Z80의 IM 2나 8086의 IVT 대신, 단일 trap vector + cause register로 푼다. 30줄 안에 끝난다. RISC-V의 trap 메커니즘을 8비트로 축소한 결정. 이 한 가지가 1980년대 RISC 결정의 가장 깊은 자리 중 하나다.

넷째, **Fibonacci 비교 표에 다섯 번째 줄을 추가했다.** RISC-8이 8080·6502·Z80·8086과 같은 표에 한 줄로 들어간다. 라인 수의 가독성과 사이클 수의 효율이 서로 다른 차원이라는 사실이 손에 잡힌다. 1980년대 RISC가 왜 이겼는지를 우리 ISA로 직접 보였다.

다섯째, **ADR로 결정을 GitHub에 남겼다.** 여섯 개 결정의 컨텍스트와 결과를 표준 양식으로 적어두었다. 책 한 권에 묻혀 사라지는 게 아니라 GitHub에 영구적으로 남는다. 후일 누군가가 RISC-8을 펴 봤을 때 "이 사람들이 왜 이렇게 결정했는가"를 손에 쥐도록.

기억해두자. **우리가 짠 RISC-8 ISA는 책에 한 번 적히고 사라지지 않는다.** GitHub에 16개 명령어의 정확한 인코딩, sealed class 구현, 어셈블러, Fibonacci 예제, 여섯 개 ADR이 함께 남는다. 누군가가 그 위에 자기 변주를 더하면, 그게 RISC-8 v2가 될 수도 있다. **ISA가 살아 있는 무엇이 될 수 있다는 점**, 그게 ISA 설계의 정서적 절정이다. 4부 끝에서 우리가 손에 쥔 가장 깊은 자리가 여기다.

자, 4부의 끝이다. 한 발 멈춰서 정리해보자.

- 11장에서 같은 Fibonacci를 8080·6502·Z80·8086 네 가지 어셈블리로 비교했다.
- 12장에서 1980년대 RISC vs CISC 논쟁을 역사로 펴 봤다.
- 13장에서 우리만의 8비트 RISC ISA — RISC-8 — 를 설계했다.

**4부 끝에서 우리는 1980년대 ISA 설계 논쟁을 손에 익히고, 우리 자신의 ISA를 짠 한 사람이 되었다.** 14주 동안의 산행을 정리하는 한 줄이다. 5부로 넘어가면 우리는 RISC-8을 cycle-accurate로 다시 짠다. IPC ≈ 1이라는 RISC의 약속을 손으로 검증한다. 그러고 나서 마지막 15장에서 — **"여기서 어디로 갈 것인가"** — 우리 8비트 우주 다음의 컴퓨터 전체를 향한 다리를 본다. 같이 가 보자.

> **GitHub 산출물**
>
> - 파일: `chapter-13/risc8/IsaSpec.md`(16개 명령어 인코딩 명세), `Risc8Core.kt`(150줄), `Risc8Assembler.kt`, `TrapVector.kt`(인터럽트), `examples/fibonacci.asm`
> - ADR: `adr/001-fixed-16bit-encoding.md` 부터 `adr/006-single-trap-vector.md`까지 여섯 개
> - 테스트: `Risc8CpuTest.kt`(~30개), `AssemblerTest.kt`(~10개), `FibonacciE2ETest.kt`(1개 — n=10이 정확히 55를 낸다)
> - 실행: `./gradlew :chapter-13:test`, `./gradlew :chapter-13:run -PfibN=10` (Fibonacci 데모)
> - 책의 가장 창의적인 산물. 14장에서 RISC-8을 cycle-accurate로 다시 짠다.
