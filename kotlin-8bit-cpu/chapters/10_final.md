<!-- 개정: 2026-05-13 style-guardian 라운드 1 반영 — Should 1·2·4·5 (3·6은 칭찬 메모) -->

# 10장. 마이크로코드와 디버거 — 하드웨어를 소프트웨어로 묘사한다

자기가 짠 SAP-2 위에서 7바이트짜리 짧은 프로그램을 돌렸는데 출력이 틀린 광경을 상상해보자. `LDA 10 ; ADD 11 ; JZ skip ; OUT ; HLT` 정도의 수십 줄도 안 되는 코드인데 마지막에 0이 찍힌다. 분명 3과 5를 더한 결과는 8이 나와야 했다. 어디서부터 짚어야 할까?

가장 먼저 떠오르는 길은 `println()`이다. 어셈블러의 출력을 보고, 메모리 덤프를 찍고, 실행 후 A 레지스터를 찍어 본다. 그러나 그 어디에도 답이 없다. A에 들어간 값은 분명 0x08인데, 출력 레지스터에는 0이 적혀 있다. **그 사이에 무슨 일이 있었나?** 9장에서 우리가 잘못 짠 어떤 분기 명령어가 의도와 달리 점프를 해 버린 것일까? 점프하기 직전의 ALU 플래그는 어떤 상태였나? 그 사이에 컨트롤러가 어느 마이크로코드 줄을 발화시켰나?

`println`으로는 이 질문에 답할 수 없다. 우리는 CPU 안의 사이클 단위 흐름을 들여다보고 싶다. **한 명령어가 끝나는 동안 컨트롤러가 어떤 control signal을 어떤 순서로 켰는지**, **그 사이에 레지스터들이 어떻게 변했는지**, 가능하면 **명령어 한 줄, 한 줄이 시작할 때 멈춰 서서 직접 들여다보고 싶다**. 정말 답답한 일이다. CPU 안을 직접 들여다볼 수 없으면 그 안의 버그는 거의 영원히 못 잡는다.

이 장에서 우리는 두 가지를 손에 쥔다. 하나는 **마이크로코드** — 컨트롤러를 회로가 아니라 ROM으로 다시 짜는 길이다. control signal의 시퀀스를 enum과 비트마스크로 옮기고, 명령어가 시작될 때마다 그 시퀀스를 한 줄씩 발화시킨다. 9장에서 짠 SAP-2 컨트롤러가 이미 그렇게 일하고 있었는데, 이 장에서 우리는 그 ROM을 정면으로 들여다보고 직접 수정한다. 또 하나는 **디버거** — breakpoint, step, register dump, memory dump 같은 도구들을 우리 손으로 짠다. GDB가 일하는 방식의 가장 단순한 형태가 어떻게 생겼는지 손에 잡힐 것이다.

이 두 가지가 만나면 **우리가 짠 SAP-2의 내부를 한 사이클씩 들여다보는 도구**가 완성된다. 3부의 정서적 절정이다. 자기 CPU의 마이크로코드를 직접 읽고, 직접 고치고, 직접 한 박자씩 멈춰 서서 들여다본다. 컴퓨터를 만든다는 일의 가장 깊은 즐거움이 여기에 있다. 같이 가 보자.

## 10.1 하드와이어드의 한계 — SAP-1 컨트롤러를 다시 펴 본다

마이크로코드가 무엇인지 이해하기 전에 한 발 뒤로 가서 우리가 6장에서 짠 SAP-1의 컨트롤러를 다시 펴 보자. 그것이 어떤 길이었고, 왜 그 길로는 더 못 가는지가 SAP-2의 마이크로코드를 만나는 자연스러운 진입로다.

SAP-1의 컨트롤러는 매우 단순했다. 한 사이클마다 6개의 T-state가 돌아간다. 각 T-state에서 컨트롤러는 어떤 control signal을 켜고 어떤 것을 끌지를 결정한다. 명령어가 5개 — LDA, ADD, SUB, OUT, HLT — 였고, 각 명령어는 6 T-state짜리 시퀀스를 갖는다. 5 × 6 = 30개의 control signal 묶음. 이것을 `when` 표현식으로 손으로 짰다. 한 줄로 표현하면 이런 모양이었다.

```kotlin
// SAP-1 컨트롤러의 핵심 부분 (6장에서 짠 형태)
fun tStateSignals(opcode: Int, tState: Int): Set<ControlSignal> = when (opcode) {
    0x10 -> when (tState) {  // LDA
        0 -> setOf(CO, MI)
        1 -> setOf(RO, II, CE)
        2 -> setOf(IO, MI)
        3 -> setOf(RO, AI)
        4 -> emptySet()
        5 -> emptySet()
        else -> error("invalid t-state")
    }
    0x20 -> when (tState) {  // ADD
        // 비슷하게 6줄 ...
    }
    // ... SUB, OUT, HLT까지
}
```

이게 **하드와이어드 컨트롤** 방식이다. control signal 시퀀스가 코드의 한 부분으로 박혀 있다 — "박혀 있다"는 비유가 정확히 들어맞는다. 하드웨어로 짠다면 게이트와 신호 라인의 조합이 그 자리에 박혀 있을 것이고, 우리는 Kotlin 코드의 `when` 표현식이라는 형태로 그것을 옮겼다.

이 방식의 매력은 무엇이었나? **빠르다.** ROM에서 한 줄 더 읽어올 필요가 없다. 한 클록 안에서 조합 논리가 그대로 답을 내놓는다. 그리고 **구현이 직관적이다.** 우리가 6장에서 본 그대로다 — 명령어마다 6줄짜리 `when` 가지를 하나씩 추가하면 그만이었다.

그런데 SAP-2로 넘어오면서 사정이 달라졌다. 명령어가 5개에서 **39개**로 늘었다. T-state도 명령어마다 다른 길이를 가질 수 있다 — `MOV B, A` 같은 단순 명령어는 4 T-state로 끝나고, `CALL addr` 같은 복잡한 명령어는 10 T-state 이상 걸린다. control signal도 12개에서 **35개**로 늘었다. 39 × 10 × 35 = **13,650개의 비트**를 한 표에 적어야 한다.

이걸 6장 스타일의 `when` 표현식으로 짜자고 들어보자. 정말 끔찍한 일이다. 명령어 하나를 추가할 때마다 거대한 `when` 분기에 또 하나의 가지를 더한다. 그러다가 한 명령어의 T-state 5번에 `BI` 신호를 켜야 하는데 실수로 안 켰다면? 그 버그를 찾으려고 컨트롤러 코드 전체를 한 줄씩 다시 읽어야 한다. 한 명령어를 추가하는 게 아니라 한 ISA를 통째로 다시 짜는 일에 가까워진다. 이게 마이크로프로그래밍이 등장한 자리다.

여기서 한 가지 다른 길이 등장한다. **컨트롤러를 ROM으로 짜자.** control signal 시퀀스를 코드가 아니라 데이터로 본다. 그러면 컨트롤러의 본문은 매우 단순해진다 — 그저 ROM의 한 줄을 읽어서 그 비트들을 control signal로 발화시키면 그만이다. 명령어가 늘어나도 컨트롤러 코드는 손대지 않는다. ROM의 데이터만 늘리면 된다. 이게 **마이크로프로그래밍**이다.

> **사이드바: Maurice Wilkes의 1951년 한 줄**
>
> 마이크로프로그래밍이라는 아이디어는 1951년 영국 케임브리지의 Maurice Wilkes가 한 짧은 논문에서 제안했다. 제목은 "The Best Way to Design an Automatic Calculating Machine." 그 시점에는 EDSAC을 막 작동시키고 다음 세대 컴퓨터를 설계하던 중이었다. Wilkes의 통찰은 단순했다 — "컨트롤러를 두 단계로 나누자. 사용자가 보는 ISA(매크로 레벨)와, 그 안에서 실행되는 마이크로 명령어 레벨(micro level). 매크로 명령어 하나가 발화될 때, micro 레벨의 작은 시퀀스가 ROM에서 읽혀 실행된다." 이 한 줄이 이후 IBM System/360(1964) 시리즈를 비롯한 모든 메인프레임의 컨트롤러 설계에 정착했다. 우리가 짤 SAP-2 마이크로코드는 정확히 같은 아이디어를 따른다. 70년이 지나도 살아 있는 아이디어다.

## 10.2 마이크로 명령어란 무엇인가

자, 마이크로코드를 코드로 옮기기 전에 한 가지 개념을 또렷이 잡자. **마이크로 명령어 한 줄이란 무엇인가?**

답은 단순하다. **한 클록 동안 켜져 있어야 할 control signal들의 집합.** 그게 마이크로 명령어 한 줄이다. 예를 들어 SAP-2의 `MOV B, A` 명령어의 T-state 3에서 켜져야 할 신호가 `AO`(A의 값을 W-bus로)와 `BI`(W-bus의 값을 B로) 두 개라면, 그 T-state의 마이크로 명령어는 `{AO, BI}`다. 한 묶음의 신호들. 그 외의 모든 신호는 꺼져 있다.

이 묶음을 데이터로 표현하는 가장 자연스러운 길은 **비트마스크**다. 35개의 control signal이 있다면 35비트짜리 묶음 하나로 한 T-state의 마이크로 명령어를 적는다. Kotlin에서는 35비트는 `Long`(64비트) 하나에 충분히 들어간다. 또는 `EnumSet`(자바 표준 라이브러리)으로 더 가독성 있게 적을 수도 있다. 둘의 트레이드오프가 있는데, 잠시 후에 본격적으로 살펴보자.

전체 ROM의 모양은 어떻게 되나? **(opcode × T-state) → 마이크로 명령어**의 표다. 39개 명령어 × 10 T-state = 390개의 항목. 각 항목이 35비트 묶음. 이걸 Kotlin으로 옮기면 한 줄이 된다.

```kotlin
typealias MicroInstruction = Long   // 35비트 신호 묶음

class MicroRom {
    private val rom: Map<Pair<Int, Int>, MicroInstruction> = buildRom()
    //                  ^^^^^^^^^^^^^^^^^^^
    //                  (opcode, tState) → 마이크로 명령어

    fun signalsAt(opcode: Int, tState: Int): MicroInstruction =
        rom[opcode to tState] ?: 0L  // 정의 안 된 T-state는 신호 없음
}
```

이 한 줄짜리 인터페이스가 마이크로코드 ROM의 정체다. 호출자(컨트롤러)는 그저 "지금 어떤 opcode의 어떤 T-state다, 신호 묶음 줘"라고 묻고, ROM은 데이터 한 줄을 꺼내준다. 컨트롤러의 본문은 이제 매우 단순해진다.

```kotlin
class Controller(private val rom: MicroRom) {
    fun tick(opcode: Int, tState: Int): MicroInstruction =
        rom.signalsAt(opcode, tState)
}
```

명령어가 늘어나도 이 `tick`은 손대지 않는다. ROM의 `rom` 맵만 늘리면 된다. control signal이 추가되어도 비트마스크의 비트 자리만 잡으면 된다. 이게 마이크로프로그래밍이 우리에게 주는 선물이다. **컨트롤러의 본문이 ISA의 변화로부터 거리를 둔다.**

## 10.3 Kotlin으로 SAP-2 마이크로코드 ROM 짜기

이제 본격적으로 짜 보자. 먼저 35개 control signal을 enum으로 정리한다. SAP-2의 정확한 35개 signal 목록은 Malvino 명세를 따라가지만 다음과 같은 그룹으로 나뉜다.

```kotlin
enum class ControlSignal {
    // 출력 신호 (W-bus로 값을 내보냄, "Out" 의미)
    AO, BO, CO, ALO, FO,         // A/B/C/ALU/Flag 출력
    PCO, MARO, MDRO, IRO,        // PC/MAR/MDR/IR 출력

    // 입력 신호 (W-bus에서 값을 받음, "In" 의미)
    AI, BI, CI, FI,              // A/B/C/Flag 입력
    PCI, MARI, MDRI, IRI,        // PC/MAR/MDR/IR 입력

    // ALU 연산 코드 (3비트로 8가지 연산)
    ALU_ADD, ALU_SUB, ALU_AND, ALU_OR, ALU_XOR, ALU_NOT, ALU_INC, ALU_DEC,

    // 메모리 제어
    MEM_READ, MEM_WRITE,

    // PC 제어
    PC_INC,

    // 출력 레지스터
    OUT_LATCH,

    // 시퀀서
    HLT_LATCH, T_RESET,

    // 인터럽트 (옵션, 11장에서)
    INT_ACK, INT_DISABLE, INT_ENABLE,

    // 예약 (확장용)
    RESERVED_1, RESERVED_2;
}
```

35개를 한 묶음으로 본다 — 정확한 자리는 SAP-2 명세를 따라가되 우리 책의 분류로 묶었다. enum으로 정리하니까 코드 어디서나 `ControlSignal.AO`처럼 자기 이름으로 부를 수 있다. 매직 넘버가 없다. 이것이 enum의 미덕이다.

다음은 마이크로 명령어를 enum 묶음으로 표현하는 작은 도우미.

```kotlin
fun Set<ControlSignal>.toMask(): Long {
    var mask = 0L
    for (signal in this) {
        mask = mask or (1L shl signal.ordinal)
    }
    return mask
}

infix fun Long.has(signal: ControlSignal): Boolean =
    (this and (1L shl signal.ordinal)) != 0L
```

`Set<ControlSignal>.toMask()`는 enum 묶음을 `Long` 비트마스크로, `Long has signal`은 비트마스크에서 한 신호의 존재 여부를 확인한다. 이 두 줄짜리 도우미 덕분에 본문에서는 enum의 가독성과 비트마스크의 성능을 동시에 누릴 수 있다.

이제 ROM의 본체를 짜자. 모든 39개 명령어를 한 번에 적자면 너무 길어지니, 대표적인 몇 개를 골라 짠다.

```kotlin
class MicroRom {
    private val rom: Map<Pair<Int, Int>, Long> = buildRom()

    private fun buildRom(): Map<Pair<Int, Int>, Long> {
        val rom = mutableMapOf<Pair<Int, Int>, Long>()

        // 모든 명령어가 공통으로 갖는 fetch 사이클 (T0~T2)
        val FETCH = listOf(
            setOf(PCO, MARI),                  // T0: PC → MAR
            setOf(MEM_READ, MDRI, PC_INC),     // T1: 메모리 read → MDR, PC++
            setOf(MDRO, IRI)                   // T2: MDR → IR
        )

        // MOV B, A — opcode 0x47
        // T3: A → W-bus → B
        val MOV_B_A = FETCH + listOf(
            setOf(AO, BI, T_RESET)
        )
        installInstruction(rom, opcode = 0x47, micro = MOV_B_A)

        // ADD B — opcode 0x80
        // T3: A → ALU input1, B → ALU input2, ADD signal
        // T4: ALU 출력 → A, T_RESET
        val ADD_B = FETCH + listOf(
            setOf(AO, BO, ALU_ADD),
            setOf(ALO, AI, FI, T_RESET)
        )
        installInstruction(rom, opcode = 0x80, micro = ADD_B)

        // JMP addr — opcode 0xC3
        // T3: PC → MAR (다음 두 바이트가 점프 주소)
        // T4: MEM_READ → MDR (low byte)
        // T5: MDR → PC low
        // T6: PC++ → MAR
        // T7: MEM_READ → MDR (high byte)
        // T8: MDR → PC high, T_RESET
        // (실제로는 더 단순한 인코딩으로 줄일 수 있다)
        val JMP = FETCH + listOf(
            setOf(PCO, MARI),
            setOf(MEM_READ, MDRI, PC_INC),
            setOf(MDRO, PCI),   // 단순화: 8비트 PC 가정
            setOf(T_RESET)
        )
        installInstruction(rom, opcode = 0xC3, micro = JMP)

        // HLT — opcode 0x76
        val HLT = FETCH + listOf(
            setOf(HLT_LATCH, T_RESET)
        )
        installInstruction(rom, opcode = 0x76, micro = HLT)

        // ... 나머지 35개 명령어를 같은 방식으로

        return rom
    }

    private fun installInstruction(
        rom: MutableMap<Pair<Int, Int>, Long>,
        opcode: Int,
        micro: List<Set<ControlSignal>>
    ) {
        for ((t, signals) in micro.withIndex()) {
            rom[opcode to t] = signals.toMask()
        }
    }

    fun signalsAt(opcode: Int, tState: Int): Long =
        rom[opcode to tState] ?: 0L
}
```

이 코드의 매력은 **마이크로 명령어 시퀀스가 데이터처럼 읽힌다**는 점이다. `MOV_B_A`라는 변수가 그 명령어의 한 사이클을 표현한다. 그 변수의 값을 들여다보면 "fetch 3 사이클 + 명령어 자체의 1 사이클"이라는 구조가 또렷이 보인다. 이게 마이크로프로그래밍이 만든 가독성이다.

테스트도 짜 두자. ROM이 우리가 적은 그대로 동작하는지 확인하는 것이 마이크로코드를 디버깅하는 가장 안전한 방법이다.

```kotlin
class MicroRomTest : FunSpec({
    val rom = MicroRom()

    test("모든 명령어의 fetch 사이클(T0~T2)이 동일하다") {
        val opcodes = listOf(0x47, 0x80, 0xC3, 0x76)  // MOV B,A / ADD B / JMP / HLT
        for (op in opcodes) {
            rom.signalsAt(op, 0) shouldBe setOf(PCO, MARI).toMask()
            rom.signalsAt(op, 1) shouldBe setOf(MEM_READ, MDRI, PC_INC).toMask()
            rom.signalsAt(op, 2) shouldBe setOf(MDRO, IRI).toMask()
        }
    }

    test("MOV B, A의 T3는 AO + BI다") {
        val signals = rom.signalsAt(0x47, 3)
        (signals has AO) shouldBe true
        (signals has BI) shouldBe true
        (signals has T_RESET) shouldBe true
        (signals has CI) shouldBe false   // C로 가는 신호는 켜져 있으면 안 된다
    }

    test("ADD B의 T4에 ALO와 AI가 함께 켜진다") {
        val signals = rom.signalsAt(0x80, 4)
        (signals has ALO) shouldBe true
        (signals has AI) shouldBe true
        (signals has FI) shouldBe true   // 플래그도 함께 업데이트
    }

    test("정의되지 않은 T-state는 0을 반환한다") {
        rom.signalsAt(0x47, 9) shouldBe 0L
    }
})
```

이 네 테스트가 ROM의 핵심 동작을 안전 그물로 감싼다. 마이크로코드를 손으로 적는 일은 실수가 잦다 — 비트 자리 하나 빠뜨리는 게 사람의 일이다. 그때 이 테스트가 빨간 줄을 내며 우리를 깨운다. 정말 고마운 친구다.

## 10.4 마이크로코드 시퀀스의 디버그 출력 — 사이클을 글로 옮긴다

ROM이 동작한다는 사실은 테스트로 확인했다. 그런데 실제로 명령어가 실행되는 동안 어떤 신호가 어떤 순서로 발화되는지를 사람의 눈으로 확인하는 도구가 있으면 더 편하지 않을까? 이게 디버그 출력의 첫 형태다.

```kotlin
class MicroTracer(private val rom: MicroRom) {
    fun trace(opcode: Int): String {
        val sb = StringBuilder()
        sb.appendLine("=== opcode 0x${opcode.toString(16).uppercase().padStart(2, '0')} ===")
        for (t in 0..9) {
            val signals = rom.signalsAt(opcode, t)
            if (signals == 0L) break
            sb.appendLine("T$t: ${decodeMask(signals)}")
        }
        return sb.toString()
    }

    private fun decodeMask(mask: Long): String =
        ControlSignal.values()
            .filter { mask has it }
            .joinToString(", ") { it.name }
}
```

`MOV B, A`의 트레이스를 한 번 찍어 보자.

```
=== opcode 0x47 ===
T0: PCO, MARI
T1: MEM_READ, MDRI, PC_INC
T2: MDRO, IRI
T3: AO, BI, T_RESET
```

네 줄이다. 명령어 한 줄이 4 T-state에서 끝난다. 이 트레이스를 직접 보면 "MOV B, A가 정확히 무슨 일을 하는가"가 손에 잡힌다. fetch 3 사이클 동안 명령어 자체를 메모리에서 꺼내고, T3에서 A를 W-bus로 보내 B에 적는다. 단지 그것뿐이다. **한 줄의 어셈블리어가 4개의 마이크로 명령어로 풀어진다.** 이 풀어진 모습을 글로 옮긴 게 트레이스의 정체다.

> **사이드바: x86은 내부에서 RISC처럼 돈다**
>
> 현대 x86 CPU 안에서는 사실 우리가 짠 SAP-2와 비슷한 일이 일어난다. `ADD EAX, [EBX+8]` 같은 CISC 명령어가 들어오면, CPU의 디코더가 그것을 3~4개의 **micro-op**(μop)으로 풀어낸다. 메모리 로드 μop, 레지스터 덧셈 μop, 그리고 결과 저장 μop. 그 μop들이 실제로는 RISC-like한 단순한 형태로 파이프라인을 흐른다. 1980년대 RISC vs CISC 논쟁의 한 결론이 여기에 있다 — x86은 인터페이스(ISA)는 CISC이지만 **내부는 RISC**다. 마이크로코드의 진화형이다. 우리가 짠 SAP-2 마이크로코드의 한 줄이 바로 그 μop의 8비트 시대 조상이다. 12장에서 RISC 논쟁을 만날 때 이 사이드바를 다시 펴 보자.

자, 이제 마이크로코드를 데이터로 들여다보는 도구가 손에 들어왔다. 그런데 우리가 정작 짜고 싶은 것은 마이크로코드를 보는 게 아니라 **명령어가 실행되는 흐름**을 보는 일이다. 명령어 한 줄이 끝났을 때 레지스터의 상태가 무엇이고, 그다음 명령어가 시작되기 직전에 어디서 멈춰서 들여다보고 싶다. 그게 디버거의 일이다. 가 보자.

## 10.5 디버거 짜기 — breakpoint, step, dump

디버거는 사실 굉장히 단순한 도구다. 우리가 GDB나 IntelliJ의 디버거에서 매일 보는 그 거대한 UI도, 그 안에서 일하는 핵심은 다음 네 가지 동작으로 환원된다.

1. **step**: 명령어를 한 줄만 실행하고 멈춘다.
2. **breakpoint**: 특정 메모리 주소에 도달하면 실행을 멈춘다.
3. **register/memory dump**: 멈춘 상태에서 레지스터와 메모리를 출력한다.
4. **continue**: 멈춘 곳부터 다시 실행한다 (breakpoint를 만날 때까지).

step-over, step-into, watch expression 같은 고급 기능은 사실 위 네 가지를 조합해서 만든다. 우리는 이 네 가지를 손으로 짜자. 이게 디버거의 가장 단순한 형태다.

```kotlin
class Debugger(private val cpu: Sap2) {
    private val breakpoints = mutableSetOf<Int>()
    private var halted = false

    fun setBreakpoint(addr: Int) {
        breakpoints += addr
    }

    fun clearBreakpoint(addr: Int) {
        breakpoints -= addr
    }

    /** 명령어 한 줄만 실행한다. */
    fun step(): StepResult {
        if (cpu.halted) return StepResult.Halted
        cpu.stepInstruction()   // 9장에서 짠 SAP-2의 한 명령어 실행
        return StepResult.Stepped(cpu.pc.value)
    }

    /** breakpoint를 만날 때까지 실행한다. */
    fun continueRun(maxSteps: Int = 100_000): RunResult {
        var steps = 0
        while (!cpu.halted && steps < maxSteps) {
            if (cpu.pc.value in breakpoints && steps > 0) {
                return RunResult.HitBreakpoint(cpu.pc.value)
            }
            cpu.stepInstruction()
            steps++
        }
        return if (cpu.halted) RunResult.Halted else RunResult.TimedOut
    }

    fun dumpRegisters(): String = """
        A   = 0x${cpu.a.value.toHex()}
        B   = 0x${cpu.b.value.toHex()}
        C   = 0x${cpu.c.value.toHex()}
        PC  = 0x${cpu.pc.value.toHex(4)}
        SP  = 0x${cpu.sp.value.toHex(4)}
        F   = ${cpu.flags.describe()}    (Z=${cpu.flags.zero} C=${cpu.flags.carry} S=${cpu.flags.sign})
        OUT = 0x${cpu.out.value.toHex()}
    """.trimIndent()

    fun dumpMemory(start: Int, length: Int): String {
        val sb = StringBuilder()
        for (offset in 0 until length step 8) {
            sb.append("0x${(start + offset).toHex(4)}: ")
            for (i in 0 until 8) {
                val byte = cpu.memory[start + offset + i]
                sb.append("${byte.toHex()} ")
            }
            sb.appendLine()
        }
        return sb.toString()
    }
}

sealed class StepResult {
    data class Stepped(val newPc: Int) : StepResult()
    object Halted : StepResult()
}

sealed class RunResult {
    data class HitBreakpoint(val addr: Int) : RunResult()
    object Halted : RunResult()
    object TimedOut : RunResult()
}
```

핵심은 `step()`과 `continueRun()` 두 함수다. step은 한 명령어만 돌리고, continueRun은 breakpoint를 만날 때까지 돈다. dumpRegisters와 dumpMemory는 멈춘 시점의 상태를 보여 준다. 이걸로 충분하다. GDB가 보여 주는 화려한 기능들도 결국 이 네 가지의 조합이다.

이걸 어떻게 쓰는지 한 번 보자. 예를 들어 우리가 짠 잘못된 분기 코드를 디버깅한다고 해 보자.

```kotlin
fun main() {
    // 1. SAP-2를 띄우고 디버거에 연결
    val cpu = Sap2()
    val program = Assembler().assemble("""
        LDA 0x20
        ADD 0x21
        JZ  skip       ; 결과가 0이면 점프 (3+5=8이라 점프하면 안 됨)
        OUT
        HLT
        skip:
        XRA A          ; A를 0으로 (의도된 동작이지만 여기 오면 안 됨)
        OUT
        HLT
    """.trimIndent())
    cpu.loadProgram(program)
    cpu.memory[0x20] = 0x03
    cpu.memory[0x21] = 0x05

    val dbg = Debugger(cpu)

    // 2. JZ 명령어 직전에 breakpoint
    dbg.setBreakpoint(addr = 0x04)  // JZ 자리 가정

    // 3. 실행하고 breakpoint에서 멈춘다
    val result = dbg.continueRun()
    println("Stopped at: $result")

    // 4. 멈춘 시점의 레지스터 상태를 본다
    println(dbg.dumpRegisters())
    // 만약 A = 0x08이고 Z = false라면 점프하지 않아야 정상
    // A = 0x00이거나 Z = true로 잘못 켜져 있으면 → 9장의 분기 조건이 잘못된 것

    // 5. 한 명령어만 더 실행해서 PC가 어디로 가는지 본다
    dbg.step()
    println("After step, PC = 0x${cpu.pc.value.toString(16)}")
    // 정상이면 OUT(주소 0x05)으로 가야 하고
    // 잘못되면 skip(주소 0x07 등)으로 점프해 버린다
}
```

이게 디버거가 우리에게 주는 힘이다. **CPU의 안을 한 사이클씩 들여다본다.** 분기 조건이 잘못 켜져 있다는 사실을 코드를 다시 읽어서 추측하는 게 아니라, **그 시점에 레지스터의 값을 직접 본다.** printf 디버깅과는 차원이 다른 도구다. 손에 들어오면 떠나기 어렵다.

테스트도 함께 짜자.

```kotlin
class DebuggerTest : FunSpec({
    test("step은 한 명령어만 실행한다") {
        val cpu = Sap2()
        cpu.loadProgram(byteArrayOf(0x3E, 0x05, 0x76))  // MOV A, 5 ; HLT
        val dbg = Debugger(cpu)

        val result1 = dbg.step()
        result1 shouldBe StepResult.Stepped(newPc = 2)   // MOV A, 5는 2바이트
        cpu.a.value shouldBe 5

        val result2 = dbg.step()
        result2 shouldBe StepResult.Stepped(newPc = 3)   // HLT는 1바이트
        // HLT 실행 후이지만 PC는 정확히 다음 위치
    }

    test("breakpoint에 도달하면 멈춘다") {
        val cpu = Sap2()
        cpu.loadProgram(byteArrayOf(0x3E, 0x05, 0x3E, 0x07, 0x76))
        //                          MOV A, 5     MOV A, 7    HLT
        val dbg = Debugger(cpu)
        dbg.setBreakpoint(2)   // 두 번째 MOV 직전

        val result = dbg.continueRun()
        result shouldBe RunResult.HitBreakpoint(2)
        cpu.a.value shouldBe 5   // 첫 번째 MOV만 실행된 상태
    }

    test("dumpRegisters는 모든 레지스터를 보여준다") {
        val cpu = Sap2().apply {
            a.value = 0x42
            b.value = 0x00
        }
        val dump = Debugger(cpu).dumpRegisters()
        dump shouldContain "A   = 0x42"
        dump shouldContain "B   = 0x00"
        dump shouldContain "PC  = 0x0000"
    }
})
```

세 테스트가 디버거의 핵심 동작을 잡는다. 9장에서 짠 SAP-2가 정확히 동작한다는 가정 위에 디버거가 얹힌다.

## 10.6 테스트 ROM — 자기 SAP-2가 자기 자신을 검증한다

디버거가 명령어 단위로 멈춰 서서 살펴보는 도구라면, **테스트 ROM**은 명령어 묶음 단위로 회귀를 잡는 도구다. 6502 세계에서는 `klaus2m5/6502_65C02_functional_tests`가 사실상의 검증 표준이다. NES 에뮬레이터들은 `nestest.nes`를 통과시키는 게 통과 의례다. Chip-8 세계는 Timendus의 test suite를 쓴다.

> "에뮬레이터를 만들면 반드시 test ROM을 돌려라. 통과시키지 못한 명령어를 그대로 두면 게임이 깨진다."
>
> — r/EmuDev 거의 만장일치 [커뮤니티-휴리스틱3]

SAP-2는 이런 표준 test ROM이 외부에 없다. 우리가 직접 짜야 한다. 정직하게 짜 보자.

```kotlin
class Sap2TestRom {
    /** 각 명령어의 정상 동작을 검증하는 짧은 프로그램들. */
    val tests: List<TestCase> = listOf(
        TestCase(
            name = "MOV A, imm; OUT — 값이 출력 레지스터에 적힌다",
            source = """
                MVI A, 0x42
                OUT 0x00
                HLT
            """.trimIndent(),
            data = emptyMap(),
            expectedOut = 0x42
        ),
        TestCase(
            name = "ADD B — 누산기 + B = A",
            source = """
                MVI A, 0x03
                MVI B, 0x05
                ADD B
                OUT 0x00
                HLT
            """.trimIndent(),
            data = emptyMap(),
            expectedOut = 0x08
        ),
        TestCase(
            name = "JZ — 결과가 0이면 점프",
            source = """
                MVI A, 0x05
                SUI 0x05    ; A = 0, Z 켜짐
                JZ  done
                MVI A, 0xFF ; 여기 오면 실패
                done:
                OUT 0x00
                HLT
            """.trimIndent(),
            data = emptyMap(),
            expectedOut = 0x00
        ),
        TestCase(
            name = "JNZ — 결과가 0이 아니면 점프",
            source = """
                MVI A, 0x05
                SUI 0x03    ; A = 2, Z 꺼짐
                JNZ done
                MVI A, 0xFF
                done:
                OUT 0x00
                HLT
            """.trimIndent(),
            data = emptyMap(),
            expectedOut = 0x02
        ),
        TestCase(
            name = "CALL/RET — 서브루틴이 정확히 돌아온다",
            source = """
                MVI A, 0x01
                CALL add_one
                CALL add_one
                CALL add_one
                OUT  0x00
                HLT
                add_one:
                INR A
                RET
            """.trimIndent(),
            data = emptyMap(),
            expectedOut = 0x04   // 1 + 3번 INR = 4
        )
        // ... 39개 명령어를 차근차근
    )

    data class TestCase(
        val name: String,
        val source: String,
        val data: Map<Int, Int>,
        val expectedOut: Int
    )
}

class Sap2TestRomTest : FunSpec({
    Sap2TestRom().tests.forEach { tc ->
        test(tc.name) {
            val cpu = Sap2()
            val program = Assembler().assemble(tc.source)
            cpu.loadProgram(program)
            for ((addr, byte) in tc.data) {
                cpu.memory[addr] = byte
            }
            cpu.run(maxCycles = 10_000)

            cpu.out.value shouldBe tc.expectedOut
        }
    }
})
```

이게 SAP-2 회귀 테스트의 골격이다. 매 명령어가 자기 짧은 프로그램으로 자기 자신을 검증한다. 새 명령어를 추가하면 `tests`에 한 항목을 더한다. 전체 ROM을 돌리는 데 1초도 안 걸린다. CI에서도 매 푸시마다 돈다. **회귀를 잡는 가장 안전한 그물.**

여기서 흥미로운 일이 일어난다. **테스트 ROM이 실패하면, 그 실패를 디버거로 들여다본다.** 두 도구가 짝을 이룬다. test 실패 → break 설정 → step으로 한 줄씩 → dumpRegisters로 상태 확인 → 마이크로코드 ROM의 해당 자리 확인 → 비트 자리 수정 → 다시 test. 이 사이클이 우리의 SAP-2를 견고하게 만든다. 한 번 이 사이클이 손에 익으면 그 어떤 8비트 CPU도 두렵지 않다.

> **사이드바: ARM Cortex-M의 마이크로코드는 어디 있나?**
>
> 현대 마이크로컨트롤러 세계에서 ARM Cortex-M 시리즈(M0, M3, M4, M7)는 **마이크로코드가 거의 없다**. 1980년대 RISC 정신을 이어 받은 ARM은 "각 명령어가 한 사이클에 가깝게 단순하게 동작해야 한다"는 입장이다. 그래서 컨트롤러를 ROM이 아니라 조합 논리에 가까운 하드와이어드로 짠다. 우리가 6장에서 SAP-1을 그렇게 짠 것과 같은 방향이다. CISC가 마이크로코드의 친구라면, RISC는 하드와이어드의 친구라고 해도 좋다. 우리가 13장에서 직접 8비트 RISC를 짤 때 이 결정을 다시 짚어볼 것이다 — 컨트롤러를 ROM으로 갈 것인가, 하드와이어드로 갈 것인가. 그때까지 SAP-2의 마이크로코드 ROM이 좋은 대조군이 되어 줄 것이다.

## 10.7 CLI로 디버거를 노출하기 — 작은 REPL

디버거가 라이브러리로 있다는 것과 사람이 손으로 명령어를 타이핑해서 쓸 수 있다는 것은 다른 차원의 경험이다. GDB는 처음부터 끝까지 CLI 위에서 살았다. 우리도 짧은 CLI를 짜자. 30줄짜리.

```kotlin
fun main() {
    val cpu = Sap2()
    val asm = Assembler()

    println("SAP-2 Debugger v0.1. Commands: load, step, run, break, regs, mem, quit")
    val dbg = Debugger(cpu)

    while (true) {
        print("(sap2dbg) ")
        val input = readlnOrNull() ?: break
        val parts = input.trim().split(Regex("\\s+"))

        when (parts.firstOrNull()) {
            "load" -> {
                val source = File(parts[1]).readText()
                val program = asm.assemble(source)
                cpu.loadProgram(program)
                println("Loaded ${program.size} bytes")
            }
            "step", "s" -> println(dbg.step())
            "run", "r" -> println(dbg.continueRun())
            "break", "b" -> {
                val addr = parts[1].removePrefix("0x").toInt(16)
                dbg.setBreakpoint(addr)
                println("Breakpoint at 0x${addr.toString(16)}")
            }
            "regs" -> println(dbg.dumpRegisters())
            "mem" -> {
                val start = parts[1].removePrefix("0x").toInt(16)
                val length = parts.getOrNull(2)?.toInt() ?: 32
                println(dbg.dumpMemory(start, length))
            }
            "quit", "q" -> return
            else -> println("?")
        }
    }
}
```

30줄. 단 30줄짜리 디버거 CLI다. 이 위에 명령어를 더 얹는 일은 어렵지 않다 — disassemble 명령어를 추가하면 6장의 디스어셈블러와 연결된다, list 명령어를 추가하면 현재 PC 주변의 코드를 보여 준다, watch 명령어를 추가하면 메모리 한 자리를 감시한다. GDB에 있는 모든 기능이 이 30줄의 확장이다.

실제로 돌려 보자.

```
$ ./gradlew :chapter-10:run
SAP-2 Debugger v0.1. Commands: load, step, run, break, regs, mem, quit
(sap2dbg) load programs/fib.asm
Loaded 23 bytes
(sap2dbg) break 0x10
Breakpoint at 0x10
(sap2dbg) run
HitBreakpoint(addr=16)
(sap2dbg) regs
A   = 0x05
B   = 0x03
C   = 0x00
PC  = 0x0010
SP  = 0x00FF
F   = -Z--    (Z=true C=false S=false)
OUT = 0x00
(sap2dbg) step
Stepped(newPc=18)
(sap2dbg) regs
A   = 0x08
...
```

이 광경이 이 장이 약속한 정서적 절정이다. **자기 손으로 짠 SAP-2의 내부를 자기 손으로 짠 디버거로 한 사이클씩 들여다본다.** 어셈블러로 짠 프로그램을 로드하고, 임의의 위치에 breakpoint를 걸고, 그 시점의 모든 레지스터와 메모리 상태를 손에 쥔다. 1970년대 미니컴퓨터의 디버거가 정확히 이렇게 동작했고, 1990년대 GDB가 같은 골격을 이어받았다. 우리가 짠 30줄의 CLI가 그 거대한 가문의 가장 단순한 후예다.

## 10.8 한 챕터를 마치며 — 3부의 끝에서

이번 장에서 우리가 손에 쥔 것을 정리해보자.

첫째, **마이크로프로그래밍**이 무엇인지 손에 잡혔다. 하드와이어드 컨트롤(코드에 박힌 신호 시퀀스)이 39개 명령어 × 35 신호 × 10 T-state 규모에서 견디지 못한다는 점을, 그래서 컨트롤러를 ROM(데이터)으로 옮기는 길이 등장했다는 점을 봤다. 1951년 Maurice Wilkes의 한 줄이 70년 동안 살아 있는 아이디어다.

둘째, **35비트 control signal**을 Kotlin enum + Long 비트마스크로 옮겼다. `Set<ControlSignal>.toMask()`와 `Long has signal` 두 줄짜리 도우미가 enum의 가독성과 비트마스크의 성능을 함께 살렸다.

셋째, **마이크로 명령어의 트레이스**를 글로 옮겼다. `MOV B, A` 한 줄이 4 T-state에 펼쳐지는 모습이 손에 잡힌다. x86의 micro-op이 이 한 줄의 직계 후손이다.

넷째, **디버거의 핵심 4동작**을 손으로 짰다. step, breakpoint, register/memory dump, continueRun. GDB의 거의 모든 기능이 이 네 가지 위에 살이 붙은 것이다. 30줄짜리 CLI로 사람이 손으로 쓸 수 있게 노출했다.

다섯째, **테스트 ROM**과 디버거가 짝을 이뤘다. 테스트 실패 → break 설정 → step으로 들여다보기 → 마이크로코드 ROM 수정 → 다시 테스트. 이 사이클이 우리의 SAP-2를 견고하게 만든다.

기억해두자. **CPU 안을 들여다볼 수 있다는 것은 CPU 안의 모든 버그가 잡힐 수 있다는 뜻이다.** 보지 못하면 못 잡고, 못 잡으면 못 고친다. 디버거가 그저 편의의 도구가 아니라 **컴퓨터 구조 학습의 본질적 도구**인 이유가 여기에 있다. 6장에서 처음 SAP-1을 돌렸을 때보다, 7장에서 어셈블러를 다 짰을 때보다, 9장에서 함수 호출을 처음 봤을 때보다 — **자기 CPU의 한 사이클을 직접 본 이 순간이 가장 깊은 자리다.** 3부의 정서적 절정이라 부르는 까닭이 여기 있다.

자, 3부의 끝이다. 한 발 멈춰서 정리해보자.

- 8장에서 SAP-1의 한계를 부딪쳤고 SAP-2의 64KB·39개 명령어 세계로 넘어왔다.
- 9장에서 조건 분기·CALL/RET·I/O 포트를 짰다.
- 10장에서 마이크로코드 ROM과 디버거를 손에 쥐었다.

**3부 끝에서 우리는 8080 subset 39개 명령어, 64KB 메모리, 3개 범용 레지스터, 마이크로코드 컨트롤러, 그리고 디버거까지 갖춘 한 대의 컴퓨터를 손에 쥐었다.** 이게 9~10주 동안의 산행을 정리하는 한 줄이다. 4부로 넘어가면 우리는 잠시 우리 SAP-2 곁을 떠난다. **실제 8비트 CPU들** — Intel 8080, MOS 6502, Zilog Z80, Intel 8086 — 을 만나러 간다. 같은 Fibonacci를 네 가지 어셈블리로 짜 보면서, 우리가 짠 SAP-2가 그 칩들의 진짜 친척이라는 사실을 직접 확인한다. 같이 가 보자.

> **GitHub 산출물**
>
> - 파일: `chapter-10/sap2/MicroRom.kt`, `chapter-10/sap2/Debugger.kt`, `chapter-10/sap2/MicroTracer.kt`, `chapter-10/sap2/Sap2DebuggerCli.kt`
> - 테스트: `MicroRomTest.kt`(4개), `DebuggerTest.kt`(3개), `Sap2TestRomTest.kt`(SAP-2 39개 명령어를 차근차근 — 1차 ~15개부터 시작)
> - 실행: `./gradlew :chapter-10:run` (디버거 CLI), `./gradlew :chapter-10:test`
> - 3부의 절정. 4부 11장에서 8080·6502·Z80·8086 실제 칩의 어셈블리 비교로 간다.
