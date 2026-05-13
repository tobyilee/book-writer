# 6장. 메모리·버스·컨트롤러 — SAP-1이 처음 돌아가는 순간

지금까지 우리는 SAP-1의 부품을 하나씩 깎아왔다. 3장에서 클록과 PC를 짰고, 4장에서 A·B 레지스터와 ALU의 가산기·감산기를 붙였고, 5장에서 overflow 플래그라는 입문자의 무덤을 테스트로 정직하게 잡아냈다. 부품은 빠짐없이 책상 위에 놓여 있다.

그런데 솔직히, 지금 시점에서 한 가지 찜찜한 것이 있지 않은가? "부품은 다 있는데 도대체 이게 어떻게 한 대의 CPU가 되는가." ALU에 두 수를 넣으면 합이 나오는 건 알겠다. PC가 +1씩 돌아가는 것도 알겠다. 그러나 그 둘이 같은 박자에 같은 무대 위에서 손을 맞잡는 순간 — 그 통합의 그림이 아직 머릿속에서 흐릿하다.

이번 자리에서 함께 그 흐릿함을 걷어내자. 메모리 16바이트를 짓고, 모듈들을 잇는 W-bus를 함수 호출로 추상화하고, 컨트롤러가 T-state 6개를 짚어가며 다른 모듈들에게 "지금 이걸 켜라, 다음엔 저걸 꺼라" 하고 외치는 절차를 코드로 옮겨본다. 그러고 나면 마지막에 짧은 5바이트 프로그램 하나를 메모리에 직접 hex로 적고, 클록 한 번을 두드리는 순간 — 우리가 만든 16바이트 우주가 처음으로 살아 움직인다. 부품이 CPU가 되는 그 순간을 함께 살펴보자.

## 모듈 지도 한 번 더 — 흐릿한 그림을 또렷이

이제까지 짠 부품을 한자리에 다시 모아보자. SAP-1의 표준 청사진은 다음 모듈들로 구성된다 [§1.3].

- **클록** — 모든 박자의 기준. 4장에서 만들었다.
- **PC** (4비트) — 다음 명령어의 주소. 3장에서 짰다.
- **MAR** (4비트) — Memory Address Register. PC나 IR이 보낸 주소를 들고 RAM에 건넨다.
- **RAM** — 16바이트. 이번 장에서 짓는다.
- **IR** — Instruction Register. RAM에서 가져온 8비트를 받아 상위 4비트(opcode)와 하위 4비트(operand)를 컨트롤러에 넘긴다.
- **컨트롤러/시퀀서** — 진짜 보스. 매 T-state마다 어떤 control signal을 켤지 결정한다.
- **A 레지스터·B 레지스터** — 4장의 산물.
- **ALU** — A와 B를 받아 합·차를 내고 Z·C·V·N 플래그를 세운다.
- **출력 레지스터** — OUT 명령어가 닿으면 결과를 외부로 내보낸다.
- **W-bus** — 위 모든 모듈을 잇는 단일 8비트 버스.

부품 목록만 적어 놓으면 머리에 잘 들어오지 않는다. 우리가 짤 코드의 그림으로 한 번 더 정리하자. 흐름은 단순하다.

> 컨트롤러가 "이 T-state에서는 PC가 버스에 자기 값을 내보내고, MAR이 그것을 받아라"라는 신호를 켠다. → PC는 버스에 값을 흘리고, MAR은 그 값을 잡는다. → 다음 T-state에는 "RAM이 MAR의 주소를 읽어 버스에 내보내고, IR이 그것을 받아라"라는 신호를 켠다. → … → 마지막 T-state에서 PC를 +1 하라고 신호를 켠다. → 다음 명령어로 넘어간다.

같은 일을 명령어마다 6번 반복한다. T1, T2, T3, T4, T5, T6 — 박자가 끝나면 한 명령어가 끝난다. SAP-1의 단순함이 바로 여기에 있다. 모든 명령어가 정확히 6 T-state로 끝난다. 8080·Z80·6502처럼 명령어마다 사이클이 들쭉날쭉하지 않다.

그렇다면 컨트롤러가 매 T-state마다 켜는 신호의 정체는 무엇인가? SAP-1 전통의 명명법으로는 12개 정도다. `Cp`(PC count up), `Ep`(PC enable, 즉 PC를 버스로 내보내라), `Lm`(MAR load), `CE`(chip enable, RAM read), `Li`(IR load), `Ei`(IR enable), `La`(A load), `Ea`(A enable), `Su`(subtract), `Eu`(ALU enable), `Lb`(B load), `Lo`(output load) — 이 정도다 [§1.3]. 각 신호는 1비트짜리 boolean이다. 매 T-state마다 어떤 신호 묶음이 켜질지를 컨트롤러가 결정한다. 그 결정 표가 바로 EEPROM lookup table — 우리 코드에서는 `Map<MicroAddress, ControlWord>`로 표현한다.

머릿속에 그림이 들어왔다면, 손을 움직이자. 부품부터 한 조각씩 깎아 합쳐가자.

## 16바이트의 우주 — RAM을 짓다

먼저 메모리부터. SAP-1의 명세는 정직하다. 16바이트. 그 이상도 그 이하도 아니다.

```kotlin
class Ram(initial: IntArray = IntArray(16)) {
    private val cells: IntArray = IntArray(16).also {
        require(initial.size <= 16) { "SAP-1 메모리는 16바이트가 최대다 (요청: ${initial.size})" }
        initial.copyInto(it)
    }

    fun read(address: Int): Int {
        val addr = address and 0x0F                 // 4비트 wrap
        return cells[addr] and 0xFF
    }

    fun write(address: Int, value: Int) {
        val addr = address and 0x0F
        cells[addr] = value and 0xFF
    }

    fun dump(): IntArray = cells.copyOf()
}
```

코드는 짧지만, 몇 가지 약속이 들어 있다. 주의해서 살펴보자.

- **주소는 항상 `and 0x0F`로 마스크.** 16바이트 메모리에 5번지를 요청하든 21번지를 요청하든 같은 5번 셀로 떨어진다. 4비트 주소 폭의 wrap-around가 자연스럽게 흉내 내진다. 2장의 미니 CPU에서 `(pc + 1) and 0x03`을 두었던 것과 정확히 같은 패턴이다 — 메모리 폭이 4비트가 됐을 뿐이다.
- **데이터는 항상 `and 0xFF`로 마스크.** 8비트 셀에 음수를 욱여넣거나 256 이상을 욱여넣어도 8비트로 정직하게 잘린다. 우리의 `Int + 마스킹` 정책의 일관된 적용이다.
- **`dump()`로 한 차례 복사본을 내놓는다.** 디버깅과 테스트를 위해 메모리의 현재 상태를 들여다볼 길을 열어둔다. 원본을 직접 노출하면 외부에서 `ram.dump()[3] = 0x99` 같은 실수가 나서 찜찜하다. 복사본이 안전하다.

> **사이드바: Ben Eater의 SRAM 칩과 우리의 IntArray**
>
> Ben Eater의 브레드보드 SAP-1은 16바이트를 위해 64K 비트 SRAM 칩(`74LS189` 16×4)을 두 개 병렬로 꽂는다. 와이어를 16가닥 꽂아 주소를 전달하고, 클럭 신호로 read·write를 동기화한다. 그 모든 디테일이 우리 `IntArray(16)` 한 줄로 추상화된다. 가독성과 학습 속도를 위해서다. 13장에서 cycle-accurate으로 옮길 때 그제야 read·write 타이밍의 미묘함을 다시 들춰볼 예정이다.

## MAR과 IR — 작은 레지스터, 큰 역할

다음은 MAR과 IR. 두 레지스터 모두 4비트(MAR)·8비트(IR)짜리 작은 그릇이지만, 컨트롤러의 시퀀스에서 가장 자주 호명된다.

```kotlin
class Mar {
    private var value: Int = 0
    fun load(address: Int) { value = address and 0x0F }
    fun get(): Int = value
}

class Ir {
    private var value: Int = 0
    fun load(byte: Int) { value = byte and 0xFF }
    val opcode: Int  get() = (value shr 4) and 0x0F
    val operand: Int get() = value and 0x0F
    fun raw(): Int = value
}
```

MAR은 정직하게 4비트만 잡는다. 주소 폭이 4비트라는 명세가 마스크 한 줄에 똑같이 박혀 있다. IR은 상위 4비트와 하위 4비트를 분리해 꺼내는 두 개의 property를 제공한다. 컨트롤러가 IR을 들여다볼 때 "이 명령어가 LDA냐 ADD냐"를 알아내려면 opcode만 보면 되고, "어디 주소에서 가져오라는 거냐"는 operand만 보면 된다.

이 구조가 머릿속에 자리 잡으면, SAP-1의 명령어 인코딩 한 줄을 자기 손으로 그릴 수 있다.

| Opcode (상위 4비트) | mnemonic | 의미 |
|---|---|---|
| `0000` | LDA addr | A ← memory[addr] |
| `0001` | ADD addr | A ← A + memory[addr] |
| `0010` | SUB addr | A ← A - memory[addr] |
| `1110` | OUT     | output ← A |
| `1111` | HLT     | 정지 |

OUT과 HLT는 operand를 쓰지 않는다 — 하위 4비트를 무시한다. LDA·ADD·SUB는 operand에 4비트 주소를 담는다. 명령어가 5개뿐이라는 점, 그리고 한 바이트 안에 모든 정보가 들어간다는 점이 SAP-1의 정수다. 2장에서 본 미니 CPU의 명령어 인코딩 — opcode 4비트 + operand 4비트 — 이 그대로 확장된 셈이다. 기억해두자. 우리는 새로운 그림을 그리는 것이 아니라, 익숙한 그림에 살을 붙이고 있을 뿐이다.

## W-bus를 함수 호출로 추상화하기

이제 가장 흥미로운 결정의 자리다. W-bus를 어떻게 코드로 옮길 것인가?

물리 CPU에서 W-bus는 8가닥의 와이어다. 어느 한 모듈이 자기 값을 그 와이어에 흘리면, 같은 박자에 enable된 다른 모듈이 그 값을 받아 자기 레지스터에 적재한다. 한 박자에 정확히 한 송신자, 그리고 한 명 이상의 수신자가 있다. 두 모듈이 동시에 enable되면 회로가 short된다. 끔찍한 일이다. 실제 CPU에서는 컨트롤러가 동시 enable을 절대 허락하지 않는다.

그렇다면 코드에서는 어떻게 흉내 낼까? 가장 직접적인 방법은 `Bus` 클래스를 두고, 어느 한 모듈이 `bus.put(value)`을 호출한 직후 다른 모듈이 `bus.read()`를 호출하는 식이다. 짧게 적어보자.

```kotlin
class Bus {
    private var value: Int = 0
    fun put(byte: Int) { value = byte and 0xFF }
    fun read(): Int = value
    fun clear() { value = 0 }
}
```

극도로 단순하다. 그러나 이 단순함이 핵심이다. W-bus의 본질은 "한 시점에 하나의 값이 흐른다"는 것이고, 그 한 값을 mutable property로 옮긴 셈이다.

물론 이 추상화에는 한계가 있다. 실제 회로에서는 모듈이 "지금 내가 enable이다"라고 자기 결정으로 send할 수 없다. 컨트롤러의 control signal이 트랜지스터를 켜야만 송신이 일어난다. 우리 코드의 `bus.put()`은 그 마지막 단계를 추상화해버린 셈이다. 그렇다면 control signal은 어디로 갔는가? 다음 절 — 컨트롤러로 옮겨갔다.

> **사이드바: 6502 vs Z80 vs 8086의 버스 구조**
>
> SAP-1의 W-bus는 단일 8비트 버스다. 데이터·주소·제어가 시간 분할로 같은 8가닥을 공유한다. 실제 8비트 CPU는 어떨까?
> - **MOS 6502**: 데이터 8비트, 주소 16비트가 분리된 별개의 버스. 동시에 흐른다.
> - **Zilog Z80**: 6502와 같이 분리. 다만 `RD`·`WR` 같은 더 풍부한 컨트롤 핀이 따로 있다.
> - **Intel 8086**: 데이터·주소가 멀티플렉스 — 같은 핀(`AD0~AD15`)이 시간 분할로 둘 다 운반한다. SAP-1의 W-bus 정신과 가깝다.
>
> SAP-1의 단일 W-bus는 의도된 단순화다. 하나의 와이어에 모든 트래픽이 통과하면 동시 enable 충돌만 막으면 컨트롤러 설계가 단순해진다. SAP-2부터는 분리 버스로 옮겨갈 예정이다.

## 컨트롤러 — T-state 6개의 의미

이제 진짜 보스 차례다. 컨트롤러는 매 클록 박자마다 12개 정도의 control signal 중 어떤 것을 켤지 결정한다. 그 결정을 표로 적어두자.

SAP-1의 표준 명령어 사이클은 다음과 같이 흐른다.

**Fetch 단계 (T1~T3) — 모든 명령어 공통.**
- T1: `Ep Lm` — PC가 버스로, MAR이 그것을 받는다.
- T2: `Cp` — PC를 +1.
- T3: `CE Li` — RAM이 MAR의 주소에서 데이터를 꺼내 버스로, IR이 그것을 받는다.

**Execute 단계 (T4~T6) — 명령어마다 다르다.**
- LDA: T4 `Ei Lm` / T5 `CE La` / T6 (idle)
- ADD: T4 `Ei Lm` / T5 `CE Lb` / T6 `Eu La`
- SUB: T4 `Ei Lm` / T5 `CE Lb` / T6 `Su Eu La`
- OUT: T4 `Ea Lo` / T5 (idle) / T6 (idle)
- HLT: T4에서 `HLT` 플래그를 세움

표만 봐서는 가슴이 답답하다. 코드로 옮겨야 손에 잡힌다.

먼저 control signal을 enum으로 잡자. EnumSet은 비트마스크의 안전한 wrapper다.

```kotlin
enum class ControlSignal {
    Cp,   // PC count up
    Ep,   // PC enable to bus
    Lm,   // MAR load from bus
    CE,   // RAM enable to bus (chip enable)
    Li,   // IR load from bus
    Ei,   // IR operand enable to bus
    La,   // A load from bus
    Ea,   // A enable to bus
    Lb,   // B load from bus
    Su,   // ALU subtract mode
    Eu,   // ALU enable to bus
    Lo,   // Output load from bus
    HLT,  // halt
}

typealias ControlWord = Set<ControlSignal>
```

그리고 EEPROM lookup table을 `Map`으로.

```kotlin
data class MicroAddress(val opcode: Int, val tState: Int)

object MicroCode {
    private val cs = ControlSignal::class

    private val fetch: Map<Int, ControlWord> = mapOf(
        1 to setOf(ControlSignal.Ep, ControlSignal.Lm),
        2 to setOf(ControlSignal.Cp),
        3 to setOf(ControlSignal.CE, ControlSignal.Li),
    )

    private val execute: Map<MicroAddress, ControlWord> = mapOf(
        // LDA (0x0)
        MicroAddress(0x0, 4) to setOf(ControlSignal.Ei, ControlSignal.Lm),
        MicroAddress(0x0, 5) to setOf(ControlSignal.CE, ControlSignal.La),
        MicroAddress(0x0, 6) to emptySet(),

        // ADD (0x1)
        MicroAddress(0x1, 4) to setOf(ControlSignal.Ei, ControlSignal.Lm),
        MicroAddress(0x1, 5) to setOf(ControlSignal.CE, ControlSignal.Lb),
        MicroAddress(0x1, 6) to setOf(ControlSignal.Eu, ControlSignal.La),

        // SUB (0x2)
        MicroAddress(0x2, 4) to setOf(ControlSignal.Ei, ControlSignal.Lm),
        MicroAddress(0x2, 5) to setOf(ControlSignal.CE, ControlSignal.Lb),
        MicroAddress(0x2, 6) to setOf(ControlSignal.Su, ControlSignal.Eu, ControlSignal.La),

        // OUT (0xE)
        MicroAddress(0xE, 4) to setOf(ControlSignal.Ea, ControlSignal.Lo),
        MicroAddress(0xE, 5) to emptySet(),
        MicroAddress(0xE, 6) to emptySet(),

        // HLT (0xF)
        MicroAddress(0xF, 4) to setOf(ControlSignal.HLT),
        MicroAddress(0xF, 5) to emptySet(),
        MicroAddress(0xF, 6) to emptySet(),
    )

    fun signalsFor(opcode: Int, tState: Int): ControlWord {
        return when (tState) {
            in 1..3 -> fetch.getValue(tState)
            in 4..6 -> execute[MicroAddress(opcode, tState)]
                ?: error("정의되지 않은 명령어 사이클: opcode=0x${opcode.toString(16)}, T=$tState")
            else -> error("T-state는 1..6 범위여야 한다 (요청: $tState)")
        }
    }
}
```

테이블이 좀 길다. 그러나 이 테이블이 SAP-1의 ISA의 정수다 — 우리가 만든 5개 명령어가 각각 어떤 마이크로 동작을 일으키는지가 한자리에 모여 있다. 새 명령어를 추가하려면 이 표에 6줄을 더 적으면 끝이다. 데이터로 분리된 덕에 컨트롤러 자체는 변하지 않는다.

> **사이드바: hardwired vs microprogrammed control unit**
>
> 우리 코드의 `Map<MicroAddress, ControlWord>` 형태는 사실 **microprogrammed** 컨트롤 유닛의 흉내다 [§1.7]. 정통 SAP-1은 하드와이어드 — 조합 논리로 trans마다 직접 신호를 만든다. 하지만 학습 관점에서 microprogrammed 표가 압도적으로 읽기 쉽다. SAP-2부터는 실제로 ROM 기반 마이크로코드를 쓰니, 우리는 한 단계 앞서가는 방식으로 살고 있는 셈이다.
>
> > "The data section is the same for both the micro-coded and hardwired approaches. The main difference between Hardwired and Microprogrammed Control Unit is that a Hardwired Control Unit is a sequential circuit... while a Microprogrammed Control Unit is a unit with microinstructions in the control memory." [§1.7]

이제 컨트롤러 본체를 짜자. 컨트롤러는 매 클록 박자마다 (1) 현재 T-state를 본다 → (2) IR의 opcode를 본다 → (3) `MicroCode`에서 그에 맞는 control word를 가져온다 → (4) 그 신호 묶음에 따라 각 모듈에게 enable·load 메서드를 호출한다. 그게 전부다.

```kotlin
class Controller(
    private val clock: Clock,
    private val pc: ProgramCounter,
    private val mar: Mar,
    private val ram: Ram,
    private val ir: Ir,
    private val a: Register,
    private val b: Register,
    private val alu: Alu,
    private val output: Register,
    private val bus: Bus,
) {
    private var tState: Int = 1
    var halted: Boolean = false
        private set

    fun tick() {
        if (halted) return
        val opcode = ir.opcode
        val signals = MicroCode.signalsFor(opcode, tState)
        bus.clear()
        applySignals(signals)
        tState = if (tState == 6) 1 else tState + 1
    }

    private fun applySignals(signals: ControlWord) {
        // 1) 송신 enable signal 처리 — 한 박자에 한 송신자.
        when {
            ControlSignal.Ep in signals -> bus.put(pc.value)
            ControlSignal.CE in signals -> bus.put(ram.read(mar.get()))
            ControlSignal.Ei in signals -> bus.put(ir.operand)
            ControlSignal.Ea in signals -> bus.put(a.value)
            ControlSignal.Eu in signals -> bus.put(alu.compute(subtract = ControlSignal.Su in signals))
        }
        // 2) 수신 load signal 처리 — 같은 박자에 여러 수신자 OK.
        if (ControlSignal.Lm in signals) mar.load(bus.read())
        if (ControlSignal.Li in signals) ir.load(bus.read())
        if (ControlSignal.La in signals) a.load(bus.read())
        if (ControlSignal.Lb in signals) b.load(bus.read())
        if (ControlSignal.Lo in signals) output.load(bus.read())
        // 3) 부수 동작.
        if (ControlSignal.Cp in signals) pc.increment()
        if (ControlSignal.HLT in signals) halted = true
    }
}
```

코드를 한 번 천천히 읽어보자. `applySignals` 안에서 세 단계로 나뉘어 있다. **(1)** 송신 enable이 켜진 모듈이 자기 값을 버스에 흘린다. `when`을 쓴 이유는 분명하다 — 한 박자에 송신자는 정확히 하나여야 하니까. 두 enable이 동시에 켜지면 첫 번째만 적용되고 나머지는 무시된다. 그런데 만약 컨트롤 테이블이 잘못 설정되어 두 송신 신호가 동시에 켜지면? 그건 잡아낼 가치가 있는 버그다. 다음 절의 테스트가 그것을 책임진다. **(2)** 수신 load 신호가 켜진 모듈이 버스에서 값을 빨아들인다. 같은 박자에 두 모듈이 동시에 load해도 문제없다 — 한쪽이 받는 동안 다른 쪽도 같은 값을 받을 수 있다. **(3)** PC 증가와 halt 같은 부수 동작은 별도로 처리한다.

`Eu`(ALU enable)에서 `alu.compute(subtract = ...)`를 호출하는 부분을 짚어두자. ALU는 매번 호출될 때마다 A와 B의 값을 가지고 계산한다. `Su` 신호가 함께 켜져 있으면 빼기, 그렇지 않으면 더하기. 4장에서 짠 ALU 인터페이스가 여기서 한 번에 깔끔하게 연결된다. 작은 추상화의 보상이 누적되는 순간이다.

## Sap1 — 모든 부품을 하나로

이제 마지막 한 조각. 모든 모듈을 한 자리에 모은 `Sap1` 클래스가 필요하다.

```kotlin
class Sap1(program: IntArray = IntArray(16)) {
    val clock = Clock()
    val pc = ProgramCounter()
    val mar = Mar()
    val ram = Ram(program)
    val ir = Ir()
    val a = Register("A")
    val b = Register("B")
    val alu = Alu(a, b)
    val output = Register("OUT")
    val bus = Bus()
    val controller = Controller(clock, pc, mar, ram, ir, a, b, alu, output, bus)

    fun run(maxTicks: Int = 1_000) {
        var ticks = 0
        while (!controller.halted && ticks < maxTicks) {
            controller.tick()
            ticks++
        }
        check(controller.halted) { "$maxTicks 박자 안에 HLT에 도달하지 못했다" }
    }

    fun outputValue(): Int = output.value
}
```

특별한 마법은 없다. 각 부품을 인스턴스화하고, 컨트롤러에게 다 묶어 건넨다. `run()`은 컨트롤러의 `tick()`을 halt가 들어올 때까지 반복한다. `maxTicks` 가드를 한 줄 두자 — 프로그램이 무한 루프에 빠지면 우리 테스트가 영원히 안 끝난다. 그건 끔찍한 일이다. 1000 박자면 16바이트 SAP-1의 어떤 정상 프로그램도 충분히 끝낸다.

이제 정말로 SAP-1이 우리 손 위에 한 덩어리로 올라왔다. 클래스 11개, 코드 200줄 안팎. 손바닥을 펴면 한 대의 CPU가 거기에 있다.

## 첫 SAP-1 프로그램 — 5바이트의 마법

이제 가장 즐거운 자리다. 메모리에 직접 hex로 5바이트짜리 프로그램을 적고, 우리가 만든 CPU 위에서 돌려보자.

프로그램: `LDA 9 → ADD A → OUT → HLT`. 메모리 9번지에 값 한 개, A번지(10번지)에 또 한 개를 두고, 두 수를 더해 콘솔에 출력한다.

```kotlin
fun main() {
    // 명령어 영역:
    //   [0] 0x09  LDA addr=9   → A = mem[9]
    //   [1] 0x1A  ADD addr=A   → A = A + mem[10]
    //   [2] 0xE0  OUT          → output = A
    //   [3] 0xF0  HLT
    // 데이터 영역:
    //   [9]  = 28 (0x1C)
    //   [10] = 14 (0x0E)
    val program = IntArray(16).also {
        it[0] = 0x09
        it[1] = 0x1A
        it[2] = 0xE0
        it[3] = 0xF0
        it[9] = 0x1C
        it[10] = 0x0E
    }
    val cpu = Sap1(program)
    cpu.run()
    println("OUT = ${cpu.outputValue()}")   // OUT = 42
}
```

`./gradlew :chapter-06:run`을 두드리면 `OUT = 42`가 콘솔에 떨어진다. 단순한 출력 한 줄 같지만, 그 한 줄이 의미하는 바를 잠시 음미하자.

우리가 클록을 직접 깎았다. PC도, RAM도, MAR도, IR도, A·B 레지스터도, ALU도, 출력 레지스터도, W-bus도, 컨트롤러도 — 전부 우리가 짰다. 그 모두가 한 박자에 손을 맞잡고, 한 명령어를 fetch하고, decode하고, execute하고, 다음 명령어로 넘어갔다. 그것을 4번 반복한 끝에 `42`라는 결과 한 줄을 우리에게 돌려주었다.

> "It's pretty amazing to see it all come together and work in the end." [§5.8]

이 말은 그저 듣기 좋은 격려가 아니다. SAP-1을 처음 자기 손으로 짜본 사람이라면 진심으로 고개를 끄덕이는 순간이다. 부품이 한 대의 컴퓨터가 되는 통합의 감각 — 그것이 이 챕터의 가장 큰 보상이다. 한 번 손에 잡으면 다시 잃지 않는다.

### OUT은 무엇을 출력하는가 — 7-segment와 콘솔 사이

잠깐 짚고 가자. 우리는 `println`으로 결과를 콘솔에 찍었지만, 원전 Malvino SAP-1의 OUT은 7-segment 디스플레이를 켜는 신호다. 출력 레지스터의 8비트가 곧장 8개의 LED·세그먼트로 연결된다. 그래서 사람은 그 LED 패턴을 눈으로 읽어 숫자로 해석한다.

우리 코드의 추상화는 그 단계를 단순화했다. 8비트 정수가 그대로 콘솔에 떨어진다. ASCII 변환도, 7-segment 디코딩도 끼어들지 않는다. 단순화의 이유는 분명하다 — 학습의 핵심은 "CPU 내부에서 비트가 어떻게 흐르는가"에 있지, "출력 장치가 어떻게 비트를 빛으로 바꾸는가"에 있지 않다. 외부 디바이스의 디테일은 8장 SAP-2에서 메모리 매핑 I/O vs 별도 포트 공간 논의를 다룰 때 본격적으로 다시 꺼낸다.

다만 마음에 한 줄 남겨두자. 우리의 `OUT = 42`는 진짜 컴퓨터의 출력 메커니즘을 한 단계 추상화한 결과다. 실제 보드에서는 그 8비트가 와이어 8가닥을 통해 LED 한 묶음에 도달한다. 우리는 그 와이어 대신 `println`을 두었을 뿐이다.

## 통합 테스트 ~15개 — CPU의 명세를 굳히자

코드가 돌아간다고 끝이 아니다. 한 명령어라도 control signal 표가 어긋나면, 다른 14개 명령어가 멀쩡해도 CPU 전체가 무너진다. 지금이 통합 테스트를 두툼하게 깔아둘 자리다.

각 명령어가 정확히 자기 일을 하는지 확인하고, 명령어가 두 개·세 개 이어졌을 때의 누적 결과를 검증하고, 컨트롤 시그널의 위반(예: 한 박자에 송신자 둘)을 잡아낸다. 15개 정도면 SAP-1의 기능을 한 바퀴 다 도는 셈이다.

```kotlin
class Sap1Test {

    private fun program(vararg pairs: Pair<Int, Int>): IntArray =
        IntArray(16).also { mem -> pairs.forEach { (addr, value) -> mem[addr] = value } }

    @Test
    fun `HLT 한 명령어가 정지를 일으킨다`() {
        val cpu = Sap1(program(0 to 0xF0))
        cpu.run()
        assertTrue(cpu.controller.halted)
        assertEquals(0, cpu.outputValue())
    }

    @Test
    fun `LDA 한 줄이 A에 값을 적재한다`() {
        // [0] LDA 0xF (mem[15])  [1] HLT  [15] = 0x2A
        val cpu = Sap1(program(0 to 0x0F, 1 to 0xF0, 15 to 0x2A))
        cpu.run()
        assertEquals(0x2A, cpu.a.value)
    }

    @Test
    fun `ADD 한 줄이 A에 누적된다`() {
        // [0] LDA 0xE  [1] ADD 0xF  [2] HLT  [14]=10 [15]=32
        val cpu = Sap1(program(0 to 0x0E, 1 to 0x1F, 2 to 0xF0, 14 to 10, 15 to 32))
        cpu.run()
        assertEquals(42, cpu.a.value)
    }

    @Test
    fun `SUB 한 줄이 A에서 뺀다`() {
        // [0] LDA 0xE  [1] SUB 0xF  [2] HLT  [14]=50 [15]=8
        val cpu = Sap1(program(0 to 0x0E, 1 to 0x2F, 2 to 0xF0, 14 to 50, 15 to 8))
        cpu.run()
        assertEquals(42, cpu.a.value)
    }

    @Test
    fun `OUT은 A의 현재 값을 출력 레지스터에 복사한다`() {
        // [0] LDA 0xF  [1] OUT  [2] HLT  [15]=99
        val cpu = Sap1(program(0 to 0x0F, 1 to 0xE0, 2 to 0xF0, 15 to 99))
        cpu.run()
        assertEquals(99, cpu.outputValue())
        assertEquals(99, cpu.a.value)        // A는 그대로 남는다 — OUT은 비파괴
    }

    @Test
    fun `LDA → ADD → OUT → HLT — Malvino 표준 데모`() {
        // [0]=0x09 LDA 9  [1]=0x1A ADD A  [2]=0xE0 OUT  [3]=0xF0 HLT  [9]=28  [10]=14
        val cpu = Sap1(program(
            0 to 0x09, 1 to 0x1A, 2 to 0xE0, 3 to 0xF0,
            9 to 28, 10 to 14,
        ))
        cpu.run()
        assertEquals(42, cpu.outputValue())
    }

    @Test
    fun `8비트 wrap — ADD 결과는 0xFF로 마스크된다`() {
        // 0xFF + 0x02 = 0x101 → 마스크 → 0x01
        val cpu = Sap1(program(
            0 to 0x0E, 1 to 0x1F, 2 to 0xF0,
            14 to 0xFF, 15 to 0x02,
        ))
        cpu.run()
        assertEquals(0x01, cpu.a.value)
    }

    @Test
    fun `SUB 결과가 음수일 때 2의 보수로 wrap된다`() {
        // 0x10 - 0x20 = -0x10 → 2의 보수 → 0xF0
        val cpu = Sap1(program(
            0 to 0x0E, 1 to 0x2F, 2 to 0xF0,
            14 to 0x10, 15 to 0x20,
        ))
        cpu.run()
        assertEquals(0xF0, cpu.a.value)
    }

    @Test
    fun `명령어 한 개는 6 T-state로 끝난다`() {
        // HLT 하나를 돌리고, 컨트롤러가 6 박자 만에 멈췄는지 확인.
        val cpu = Sap1(program(0 to 0xF0))
        var ticks = 0
        while (!cpu.controller.halted) { cpu.controller.tick(); ticks++ }
        // HLT는 T4에 halt를 세우므로 fetch 3 + execute 1 = 4 박자에 끝.
        // 즉 6박자 전부 도는 명령어와 4박자에 끝나는 HLT의 차이가 SAP-1 명세 그대로다.
        assertEquals(4, ticks)
    }

    @Test
    fun `정의되지 않은 opcode는 예외를 던진다`() {
        // opcode 0x5는 SAP-1에 없다.
        val cpu = Sap1(program(0 to 0x50, 1 to 0xF0))
        assertFailsWith<IllegalStateException> { cpu.run() }
    }

    @Test
    fun `PC는 명령어마다 정확히 +1된다`() {
        // 4개 명령어를 돌리고 나서 PC가 4를 가리키는지.
        val cpu = Sap1(program(
            0 to 0x0F, 1 to 0xE0, 2 to 0xF0, 15 to 0x05,
        ))
        cpu.run()
        assertEquals(3, cpu.pc.value)   // 마지막에 fetch된 명령어(HLT)의 다음 자리.
    }

    @Test
    fun `RAM 주소는 4비트로 wrap된다`() {
        // operand에 0xFF를 줘도 mem[15]로 해석되어야 한다 — IR이 4비트만 쓰니까.
        // (사실 IR.operand가 이미 0x0F로 마스크된다.)
        val cpu = Sap1(program(0 to 0x0F, 1 to 0xF0, 15 to 0x77))
        cpu.run()
        assertEquals(0x77, cpu.a.value)
    }

    @Test
    fun `프로그램이 무한 루프에 빠지면 안전 가드가 발동한다`() {
        // HLT 없이 ADD만 반복하면 PC가 wrap되어 같은 자리를 돈다.
        // [0] ADD 0  [1] ADD 0 ... HLT가 없다.
        val program = IntArray(16) { 0x10 }   // 전 셀이 ADD 0
        val cpu = Sap1(program)
        assertFailsWith<IllegalStateException> { cpu.run(maxTicks = 100) }
    }

    @Test
    fun `LDA 후 다른 LDA가 A를 덮어쓴다`() {
        // [0] LDA 14  [1] LDA 15  [2] HLT  [14]=11 [15]=99
        val cpu = Sap1(program(
            0 to 0x0E, 1 to 0x0F, 2 to 0xF0,
            14 to 11, 15 to 99,
        ))
        cpu.run()
        assertEquals(99, cpu.a.value)
    }

    @Test
    fun `긴 누적 — LDA 0 + ADD 4번이 정확히 누적된다`() {
        // [0]=LDA F  [1..4]=ADD F  [5]=HLT  [15]=5
        // A = 5 + 5+5+5+5 = 25
        val cpu = Sap1(program(
            0 to 0x0F, 1 to 0x1F, 2 to 0x1F, 3 to 0x1F, 4 to 0x1F, 5 to 0xF0,
            15 to 5,
        ))
        cpu.run()
        assertEquals(25, cpu.a.value)
    }
}
```

15개의 테스트가 SAP-1 명세를 한 바퀴 도는 셈이다. 정상 케이스, wrap 케이스, 예외 케이스, 그리고 무한 루프 가드까지. 이 정도면 SAP-1의 행동을 우리가 정확히 알고 있다고 말할 수 있다. 더 중요한 것은, 다음 챕터에서 어셈블러를 짤 때 이 테스트들이 우리의 안전망이 되어준다는 점이다. 어셈블러가 잘못된 바이트를 생성하면 위 테스트 중 하나가 정확히 빨갛게 변한다.

## 마무리

손에 잡힌 것을 정리하자. SAP-1의 부품 목록은 이제 모듈 지도가 아니라 200줄 코드다. 메모리는 `IntArray(16)`이고, W-bus는 8비트짜리 mutable property이며, 컨트롤러는 `Map<MicroAddress, ControlWord>`를 펼쳐가며 매 박자에 누가 송신하고 누가 수신할지를 결정한다. T-state 6개로 모든 명령어가 끝난다는 SAP-1의 단순함이 코드의 단순함으로 그대로 옮겨졌다.

기억해두자. 이 챕터의 진짜 산출물은 코드 200줄이 아니다. **부품이 한 대의 컴퓨터가 되는 통합의 감각** — 그것이 본문이다. 5바이트짜리 첫 SAP-1 프로그램이 `OUT = 42`를 돌려준 순간, 우리는 그 감각을 손에 쥐었다. 앞으로 어떤 CPU를 만나도 — SAP-2든, 8080이든, RISC-V든 — 결국 "부품·버스·컨트롤러"의 같은 골격으로 분해해 볼 수 있다. 그 분해 도구를 우리는 이번 자리에서 얻은 셈이다.

W-bus를 함수 호출로, control signal을 EnumSet으로, 마이크로코드를 `Map`으로 — 이 세 가지 추상화도 머리 한 구석에 남겨두자. 이 추상화 없이 컨트롤러를 짜려고 들면 `if-else` 70줄짜리 거대 함수가 되어 손을 댈 엄두가 안 나는 끔찍한 상태로 빠진다. 단순한 자료구조 하나가 코드의 운명을 가른다.

다음 장에서는 사람의 글이 기계어가 되는 자리를 함께 들여다보자. 우리는 `LDA 9 ; ADD A ; OUT ; HLT`라고 적었는데, 위 메모리에는 `0x09 0x1A 0xE0 0xF0`이라는 4바이트가 들어 있다. 그 변환을 자기 손으로 짜본다. 2-pass 어셈블러의 골격, 심볼 테이블, forward reference 해결 — 모두 Kotlin의 sealed class와 `when`으로 깔끔하게 풀린다. 어셈블러가 다 만들어지면, 이번 장의 5바이트 hex 프로그램을 사람이 읽는 텍스트로 다시 적고, 자기 어셈블러로 빌드해 자기 CPU 위에서 돌려본다. 그 순환이 완성되는 자리다.

> **이번 챕터의 GitHub 커밋**
>
> ```
> chapter-06/
>   build.gradle.kts
>   src/main/kotlin/sap1/
>     Ram.kt          (~25줄)
>     Mar.kt, Ir.kt   (~30줄)
>     Bus.kt          (~10줄)
>     ControlSignal.kt + MicroCode.kt   (~60줄)
>     Controller.kt   (~50줄)
>     Sap1.kt         (~30줄, main 포함)
>   src/test/kotlin/sap1/
>     Sap1Test.kt     (15개 통합 테스트)
>
> 실행:  ./gradlew :chapter-06:run         → OUT = 42
> 테스트: ./gradlew :chapter-06:test        → 15/15 passed
> ```
