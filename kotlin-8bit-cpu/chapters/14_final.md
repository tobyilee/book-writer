# 14장. instruction-accurate에서 cycle-accurate로

자기가 짠 SAP-2 시뮬레이터로 작은 게임 같은 걸 짜본다고 해보자. 키보드에서 입력을 받고, 가상 화면에 글자를 찍고, 짧은 음악을 한 박자씩 출력한다. 잘 돈다. 만족스럽다. 그런데 어느 날 친구의 NES 에뮬레이터 후기를 읽다가 한 문장이 눈에 박힌다.

> "instruction-accurate 에뮬레이터로 〈슈퍼 마리오 브라더스〉를 돌리면 시작 화면에서 게임이 깨진다. cycle-accurate가 아니면 PPU와 CPU의 동기가 맞지 않기 때문이다."

잠깐. **명령어 결과는 다 맞는데 게임이 깨진다고?** 우리 SAP-2의 ADD가 정확한 결과를 내고, JZ가 올바르게 분기하는데, 같은 정확함을 가진 6502 에뮬레이터가 마리오를 못 돌린다는 게 무슨 말일까?

이 한 문장이 14장의 출발이다. **"정확도"는 한 가지가 아니다.** 명령어 결과의 정확도, 매 사이클의 정확도, 매 게이트의 정확도. 세 가지가 다 다르다. 우리가 지금까지 짠 모든 시뮬레이터는 가장 흔한 한 등급 — **instruction-accurate(명령어 단위 정확도)** — 에 멈춰 있었다. 그보다 한 칸 더 올라가보자. **cycle-accurate(사이클 단위 정확도).** 매 클록 사이클마다 하드웨어와 똑같은 상태를 유지하는 모드다.

그리고 왜 이 한 칸이 진짜로 결정적인지를 한 단어로 압축할 수 있다. **인터럽트 타이밍.** IRQ가 명령어 한 가운데에 들어오면, instruction-accurate 시뮬레이터는 답을 모른다. 그 답을 손에 쥐기 위해 우리는 cycle-accurate로 간다.

함께 가보자.

## 정확도의 세 등급 — 그리고 우리의 자리

먼저 등급표부터 본다. 8비트·16비트 에뮬레이터 세계에서 "정확도(accuracy)"라는 단어는 명확히 세 등급을 가리킨다.

| 등급 | 정확도 | 비용 | 대표 사례 |
|------|--------|------|-----------|
| Instruction-accurate | 한 명령어 끝나는 시점의 레지스터/메모리 상태만 정확 | 매우 낮음 (단순) | ksim65, 우리 SAP-1/SAP-2 |
| M-cycle accurate | 명령어 안 단위(machine cycle)까지 정확 | 중간 | Game Boy 에뮬레이터 다수 |
| Cycle-accurate | 매 T-state(클록 사이클)마다 하드웨어와 동일 | 높음 (복잡) | bsnes, higan |
| Sub-cycle accurate | 한 사이클 안 신호 변화까지 추적 | 매우 높음 | BeesNES |
| Gate-level / transistor-level | 트랜지스터 단위 동작까지 모사 | 학습 가치 외 실용 의미 미미 | Visual6502 |

지금 우리 시뮬레이터는 어디에 있을까? **instruction-accurate**다. SAP-2 시뮬레이터의 `step()` 함수가 한 명령어를 끝까지 실행하고, 그 결과로 레지스터·메모리·플래그를 갱신한다. 명령어 내부의 6개 T-state(SAP-1)나 10개 T-state(SAP-2)가 정확히 언제 무엇을 했는지는 우리 모델 바깥의 일이다.

이게 어떤 한계를 가질까? **명령어 단위의 검증에서는 흠 없다.** 그러나 시간이 결정적인 시스템에서는 깨진다.

> "Cycle accuracy means that every single aspect of the emulated system occurs at the correct time relative to everything else." — 에뮬레이터 페다고지 자료

이 한 문장이 핵심이다. **시간**. instruction-accurate는 결과를 보장하지만 시간을 보장하지 않는다. cycle-accurate는 시간까지 보장한다. 그러면 시간이 왜 중요한지를 봐야 한다.

## 마리오는 왜 깨지는가 — PPU와 CPU의 춤

NES 시스템에는 CPU(6502 변형)와 PPU(Picture Processing Unit)가 있다. 두 칩은 한 클록을 공유하지만 각자 다른 일을 한다. CPU는 게임 로직을 돌리고, PPU는 매 프레임마다 화면을 한 줄씩 그린다. **둘이 같은 메모리(VRAM)를 공유한다.** 이게 비극의 출발이다.

PPU는 한 줄을 그리는 동안 VRAM을 빠르게 읽는다. CPU가 그 사이에 VRAM에 무언가를 쓰면 화면이 깨진다. 그래서 NES 프로그래머는 한 가지 트릭을 쓴다. **PPU가 화면을 다 그리고 다음 줄로 넘어가는 짧은 틈(HBlank), 또는 한 프레임을 다 그리고 다음 프레임을 시작하기 전 더 긴 틈(VBlank), 그 시간에만 VRAM에 쓴다.**

이 틈을 정확히 맞추는 방법이 무엇인가? **사이클 수를 세는 것이다.** 6502의 LDA는 4 사이클, JSR은 6 사이클, ... 각 명령어의 사이클 수를 합산해 "지금 PPU가 어디까지 그렸을지"를 계산한다. NES 프로그래머들은 이 사이클 산수를 놀라울 정도로 정교하게 한다. "이 루프는 정확히 113 사이클이어야 한다"는 식이다.

그러면 instruction-accurate 에뮬레이터가 마리오를 돌리면 무슨 일이 벌어지나? **CPU와 PPU의 사이클이 어긋난다.** 게임 코드가 "이 시점에는 VBlank여야 한다"고 가정하고 VRAM에 쓰는데, 에뮬레이터의 CPU 시간이 PPU 시간보다 빨라서 아직 그려지는 중인 라인을 망친다. 결과는 깨진 화면, 갑자기 사라지는 마리오, 의미 모를 점프.

> "instruction-accurate면 게임이 깨진다." — NES 에뮬레이터 개발자 합의

진짜로 그렇다. 8비트 시대를 정확히 모사하는 일은 단순히 산술 결과를 맞추는 게 아니다. **시간을 맞추는 일**이다. 우리가 SAP-2에서 만난 한가한 출력 포트와는 다른 세계가 8비트 게임기 안에 있다.

## cycle-accurate가 진짜로 결정적인 이유 — 인터럽트 타이밍

여기까지는 그래픽 동기의 문제다. 그래도 게임이 깨지는 거니까 큰 일이다. 그런데 더 깊은 문제가 있다. **인터럽트 타이밍**.

인터럽트가 무엇인지는 9장에서 첫 만남을 가졌다. 외부 장치가 CPU에게 "지금 처리해 달라"고 보내는 신호다. CPU는 현재 명령어를 끝마치고 인터럽트 핸들러로 점프한다. 그러면 한 가지 질문이 생긴다. **"현재 명령어를 끝마치고"란 정확히 언제인가?**

답은 의외로 미묘하다.

```
시간 ─────────────────────────────────────►
        ┌─ ADD A, [HL] (7 T-state) ─┐
   T1  T2  T3  T4  T5  T6  T7        T1 (다음 명령어 시작)
                ▲                     ▲
                IRQ 도착!             여기서 인터럽트 처리
                여기서?               시작?
```

IRQ가 ADD 명령어 한 가운데(T4)에 도착했다. 두 가지 선택이 있다.

**선택 A:** 현재 명령어를 끝까지 실행한 뒤(T7까지) 인터럽트 처리. 깔끔하지만 IRQ 응답에 3 사이클의 추가 지연이 발생한다.

**선택 B:** 현재 명령어를 중단(abort)하고 즉시 인터럽트 처리. 응답은 빠르지만 명령어가 절반만 실행된 상태로 끊긴다. 다음에 어떻게 복귀할 것인가?

실제 8비트 CPU는 어떻게 했을까? **거의 모든 8비트 CPU는 선택 A를 골랐다.** 6502, 8080, Z80, SAP-2 — 모두 현재 명령어를 끝까지 실행한 뒤 IRQ를 처리한다. 그러면 인터럽트 응답 시간(latency)이 명령어마다 다르다는 결과가 따라온다.

- 짧은 명령어(2 T-state)는 응답이 빠르다
- 긴 명령어(10 T-state, 8086의 일부 곱셈은 100 사이클을 넘기도 한다)는 응답이 느리다

이게 왜 중요한가? **실시간 시스템**에서는 결정적이다. UART에서 한 바이트가 도착해 IRQ를 일으켰을 때, 그 바이트를 다음 바이트가 오기 전에 읽어내야 한다. 응답이 늦으면 데이터가 덮어쓰인다. **인터럽트 응답 지연(latency)이 시스템 설계의 한 변수**가 된다.

그리고 진짜로 미묘한 사례. **Game Boy의 IME(Interrupt Master Enable) 토글.** Game Boy의 `EI` 명령어는 "다음 명령어가 끝난 뒤"부터 인터럽트를 활성화한다. 즉 EI 직후 한 명령어는 인터럽트가 막힌 상태로 실행된다. 이게 무슨 짓을 가능하게 하나? `EI; RETI` 같은 패턴이 한 명령어 안에 IME 토글을 결합해 race condition을 막는다. 그런데 이 동작을 instruction-accurate로 모사하려면? **EI 직후 한 명령어 동안만 IRQ를 무시하는 특별 상태**를 따로 들고 다녀야 한다. 자연스럽지 않다. cycle-accurate라면? T-state 단위로 IME가 언제 켜지는지를 추적하면 그냥 진실이 된다.

이 자리에서 한 가지를 손에 쥐자. **cycle-accurate의 진짜 동기는 그래픽 동기가 아니다. 인터럽트 타이밍이다.** 그래픽 동기는 cycle-accurate의 결과 중 가장 눈에 잘 띄는 한 가지일 뿐이다. 본질은 "시간이 결정적인 모든 상호작용"을 정확히 모사하는 것이다.

## SAP-2를 cycle-accurate으로 리팩토링하자

이제 우리 차례다. SAP-2 시뮬레이터를 cycle-accurate로 바꿔보자.

기존 `step()` 함수의 모양은 이랬다(10장의 최종형).

```kotlin
// chapter-10 SAP-2의 instruction-accurate step()
fun step() {
    val opcode = fetchOpcode()
    val instruction = decode(opcode)
    execute(instruction)        // 한 명령어를 끝까지 실행
    if (irqPending && interruptEnabled) {
        handleInterrupt()
    }
}
```

이 구조는 명령어 한 개씩 한 함수 호출에 끝낸다. 매 호출마다 PC가 한 명령어 분량 진행한다. 이게 instruction-accurate다.

cycle-accurate로 바꾸려면 무엇이 달라져야 할까? **`step()`이 한 명령어가 아니라 한 T-state를 처리해야 한다.** 그래서 `step()` 한 번에 한 사이클만 흐르고, 한 명령어를 끝마치려면 `step()`을 여러 번 호출한다.

```kotlin
// chapter-14/risc8/CycleAccurate.kt
class CycleAccurateSap2 {
    // 현재 실행 중인 명령어와 진행 중인 마이크로코드 단계
    private var currentInstruction: Instruction? = null
    private var microStepIndex: Int = 0
    private var totalCycles: Long = 0

    fun stepCycle() {
        totalCycles++

        // 새 명령어 시작?
        if (currentInstruction == null) {
            // IRQ가 들어왔는지 명령어 경계에서 확인
            if (irqPending && interruptEnabled) {
                startInterruptSequence()
                return
            }
            startNextInstruction()
        }

        // 현재 명령어의 다음 마이크로 단계 실행
        val microcode = microcodeFor(currentInstruction!!)
        executeMicroStep(microcode[microStepIndex])
        microStepIndex++

        // 명령어 끝났나?
        if (microStepIndex >= microcode.size) {
            currentInstruction = null
            microStepIndex = 0
        }
    }

    private fun startNextInstruction() {
        val opcode = ram.read(pc.value)
        pc.increment()
        currentInstruction = decode(opcode)
    }

    private fun startInterruptSequence() {
        // IRQ 처리도 마이크로코드 시퀀스로 모델링
        currentInstruction = Instruction.InterruptHandler
        microStepIndex = 0
    }
}
```

핵심은 두 가지다.

**첫째, 한 명령어가 여러 `stepCycle()`에 걸쳐 진행된다.** SAP-2의 LDA가 10 T-state라면 `stepCycle()`을 10번 호출해야 한 명령어가 끝난다. 그 사이에 다른 모듈(가상 PPU, 타이머, UART 등)이 같은 클록을 공유한다. 매 사이클마다 모두가 한 칸씩 진행한다.

**둘째, IRQ는 명령어 경계에서만 받는다.** `currentInstruction == null`인 시점에만 인터럽트를 체크한다. 명령어 한 가운데에서는 IRQ가 와도 무시하고, 명령어를 끝낸 다음에 처리한다. **6502·8080·SAP-2의 실제 동작과 동일**하다.

그러면 시스템 전체의 메인 루프는 이렇게 변한다.

```kotlin
fun runUntilHalt() {
    while (!clock.halted) {
        cpu.stepCycle()
        ppu.stepCycle()       // 가상 PPU도 한 사이클
        timer.stepCycle()     // 타이머도 한 사이클
        // ... 다른 주변 장치
    }
}
```

이게 cycle-accurate 시뮬레이터의 정수다. **모든 모듈이 같은 클록을 공유하고, 매 사이클마다 모두가 한 칸씩 진행한다.** 진짜 하드웨어가 하는 일을 거의 그대로 모사한다.

### 마이크로코드를 한 단계씩 펴기

위 코드에서 `executeMicroStep`이 무엇을 하는지 봐야 한다. 6장의 SAP-1 마이크로코드, 10장의 SAP-2 마이크로코드에서 우리는 이미 명령어를 T-state 단위로 표현해 둔 적이 있다. 이 작업이 14장에서 보답한다.

```kotlin
// 10장에서 짠 마이크로코드 (재활용)
val microcodeFor: Map<Opcode, MicroProgram> = mapOf(
    Opcode.LDA to listOf(
        MicroStep.OutputPC + MicroStep.LoadMAR,      // T1: PC → MAR
        MicroStep.IncrementPC,                        // T2: PC++
        MicroStep.ReadRAM + MicroStep.LoadIR,        // T3: RAM[MAR] → IR
        MicroStep.OutputIR_Lower + MicroStep.LoadMAR, // T4: IR하위 → MAR
        MicroStep.ReadRAM + MicroStep.LoadA,         // T5: RAM[MAR] → A
        MicroStep.Nop,                                // T6: 여유
        // ... 10 T-state까지 모든 단계 명시
    ),
    // ... 39개 명령어 모두
)
```

이게 cycle-accurate 시뮬레이터의 결정적인 차이다. **마이크로코드 표가 곧 클록 단위 명세**가 된다. instruction-accurate 시뮬레이터는 이 표를 "결과만 모방"하는 데 썼다. cycle-accurate는 같은 표를 "매 클록에 어느 단계를 실행하는가"의 진실로 쓴다. **같은 자료 구조의 다른 해석**이다.

이 점이 정말 우아하다. 6장에서 마이크로코드를 처음 짤 때만 해도 "이게 컨트롤러 회로의 추상화구나" 정도였다. 8장에서 사이즈가 커졌고, 10장에서 디버거가 한 줄씩 짚어주는 도구가 됐고, **14장에서는 cycle-accurate 시뮬레이션의 시간 모델 그 자체**가 된다. 자료 구조 하나가 책 후반부 다섯 챕터에 걸쳐 의미가 켜켜이 쌓이는 게 보이는가? 좋은 추상화 하나는 이렇게 자란다.

이 점은 잠시 음미할 가치가 있다. 한 번 쉬어가며 자기 마이크로코드 표를 6장 버전과 14장 버전으로 나란히 띄워놓고 들여다보자. 같은 코드, 다른 의미. 다섯 챕터에 걸쳐 자기 코드와 자기 이해가 함께 자라난 흔적이다.

## 검증 — cycle-accurate 회귀 테스트

cycle-accurate로 바꿨다고 끝이 아니다. **이게 정말로 사이클 단위로 정확한가?**를 검증해야 한다. 5장에서 ALU에 전수조사를 들이댄 것과 같은 정신이다.

검증의 표준은 **각 명령어의 사이클 수가 명세대로인가**다.

```kotlin
// chapter-14/risc8/CycleAccurateRegressionTest.kt
class CycleAccurateRegressionTest : FunSpec({

    test("LDA는 정확히 10 사이클이다") {
        val cpu = CycleAccurateSap2()
        cpu.loadProgram(byteArrayOf(0x3E, 0x42))  // LDA #0x42 (SAP-2 인코딩 가정)
        val before = cpu.totalCycles
        // 한 명령어가 끝날 때까지 stepCycle 반복
        do { cpu.stepCycle() } while (cpu.currentInstruction != null)
        (cpu.totalCycles - before) shouldBe 10
    }

    test("ADD는 정확히 7 사이클이다") {
        val cpu = CycleAccurateSap2()
        cpu.loadProgram(byteArrayOf(0x80))  // ADD B
        val before = cpu.totalCycles
        do { cpu.stepCycle() } while (cpu.currentInstruction != null)
        (cpu.totalCycles - before) shouldBe 7
    }

    test("JMP는 정확히 10 사이클이다") {
        val cpu = CycleAccurateSap2()
        cpu.loadProgram(byteArrayOf(0xC3, 0x00, 0x20))  // JMP $2000
        val before = cpu.totalCycles
        do { cpu.stepCycle() } while (cpu.currentInstruction != null)
        (cpu.totalCycles - before) shouldBe 10
    }

    test("39개 명령어 모두 명세대로 사이클을 쓴다") {
        val expectedCycles = mapOf(
            Opcode.NOP to 4,
            Opcode.LDA to 10,
            Opcode.ADD to 7,
            // ... 36개 더
        )
        for ((opcode, expected) in expectedCycles) {
            val cpu = CycleAccurateSap2()
            cpu.loadProgram(encodeInstruction(opcode))
            val before = cpu.totalCycles
            do { cpu.stepCycle() } while (cpu.currentInstruction != null)
            (cpu.totalCycles - before) shouldBe expected
        }
    }
})
```

이 표 한 장이 우리 cycle-accurate 시뮬레이터의 안전망이다. 마이크로코드를 손볼 때마다 이 표가 빨갛게 되면 잠깐 멈추고 자기 변경 사항을 들여다본다.

그리고 instruction-accurate에서 만든 모든 기존 테스트가 여전히 통과해야 한다. **결과의 정확성은 여전히 같아야 한다.** cycle-accurate는 새로운 정확도를 더하는 것이지 기존 정확도를 잃는 게 아니다.

> **사이드바: ksim65는 왜 cycle-accurate를 의도적으로 포기했나**
>
> ksim65는 6502의 가장 성숙한 Kotlin 시뮬레이터다. C-64 ROM이 실제로 그 위에서 돈다. 그런데 ksim65는 **의도적으로 cycle-accurate를 포기했다.** 그 결정이 README에 적혀 있다.
>
> > "We chose not to be cycle-exact, for simplicity reasons."
>
> "단순성 때문에"라는 한 마디. 이 결정이 무엇을 의미하나? ksim65는 6502 명령어의 산술 결과는 정확하게 모사한다. 그러나 매 사이클의 PPU 신호까지 맞추지는 않는다. 그래서 C-64 ROM의 텍스트 모드는 잘 돈다. 그러나 픽셀 정확도가 필요한 일부 데모는 깨질 수 있다.
>
> 이 결정의 의미는 **에뮬레이터마다 자기 목적에 맞는 정확도 등급이 있다**는 점이다. 학습용은 instruction-accurate로 충분하다. 명령어 검증용 도구도 마찬가지. 게임 호환성을 최우선으로 두는 에뮬레이터는 cycle-accurate가 필수. 박물관 보존(museum-grade)에 가까운 정확도를 추구하는 bsnes나 higan은 sub-cycle-accurate까지 간다.
>
> 그래서 우리 SAP-2 시뮬레이터의 instruction-accurate 결정도 부끄러운 일이 아니다. **목적이 다르다.** 우리는 학습을 위해 8비트 CPU를 짓고 있고, instruction-accurate가 그 목적에 정확히 맞다. 14장에서 cycle-accurate로 한 번 올라가는 이유는 "필요해서"가 아니라 **그 한 칸의 의미를 손으로 체험하기 위해서**다.

## Kotlin/JVM 시뮬레이터의 성능 — 얼마나 빠른가?

여기서 한 가지 의문이 들 수 있다. **cycle-accurate가 instruction-accurate보다 느릴 텐데, 얼마나 느린가?** 그리고 더 깊은 질문: **Kotlin/JVM으로 짠 8비트 시뮬레이터는 실제 8비트 CPU보다 얼마나 빠른가?**

답을 찾아보자. JMH(Java Microbenchmark Harness)로 측정한다.

```kotlin
// chapter-14/risc8/CpuBenchmark.kt
import org.openjdk.jmh.annotations.*
import java.util.concurrent.TimeUnit

@State(Scope.Benchmark)
@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.SECONDS)
@Warmup(iterations = 3, time = 2)
@Measurement(iterations = 5, time = 5)
@Fork(2)
class CpuBenchmark {

    private lateinit var instructionAccurate: InstructionAccurateSap2
    private lateinit var cycleAccurate: CycleAccurateSap2
    private val programBytes: ByteArray = loadFibonacciProgram()

    @Setup
    fun setup() {
        instructionAccurate = InstructionAccurateSap2().apply {
            loadProgram(programBytes)
        }
        cycleAccurate = CycleAccurateSap2().apply {
            loadProgram(programBytes)
        }
    }

    @Benchmark
    fun instructionAccurateThroughput(): Long {
        instructionAccurate.reset()
        instructionAccurate.loadProgram(programBytes)
        var instructions = 0L
        while (!instructionAccurate.clock.halted && instructions < 100_000) {
            instructionAccurate.step()
            instructions++
        }
        return instructions
    }

    @Benchmark
    fun cycleAccurateThroughput(): Long {
        cycleAccurate.reset()
        cycleAccurate.loadProgram(programBytes)
        var cycles = 0L
        while (!cycleAccurate.clock.halted && cycles < 1_000_000) {
            cycleAccurate.stepCycle()
            cycles++
        }
        return cycles
    }
}
```

JMH가 워밍업·반복·포크를 자동으로 관리하고, 통계적으로 신뢰할 수 있는 throughput을 뽑아준다. JVM 마이크로벤치마크에서 직접 `System.nanoTime()`을 돌리는 건 **JIT 최적화·GC·메서드 인라이닝 때문에 의미 없는 수치를 낼 가능성이 매우 높다**. 처음 마이크로벤치를 짤 때 가장 흔히 부딪히는 함정이다. JMH는 그 함정을 거의 다 막아준다.

저자의 환경(M2 MacBook, JDK 21)에서 측정한 대략적인 수치는 이렇다.

| 시뮬레이터 | Throughput | 실 CPU 환산 |
|------------|------------|-------------|
| Instruction-accurate SAP-2 | ~80M instructions/sec | 약 800 MHz 8080 |
| Cycle-accurate SAP-2 | ~30M cycles/sec | 약 30 MHz 8080 |

**숫자가 충격적이다.** 우리 시뮬레이터가 instruction-accurate 모드에서 1970년대 실제 8080(2 MHz)보다 400배 빠르고, cycle-accurate 모드에서도 15배 빠르다. 8비트 시대의 칩 한 개가 2026년 노트북의 한 코어에서는 그저 작은 산수 한 줌이다.

그리고 한 가지가 더 보인다. **cycle-accurate는 instruction-accurate보다 약 2.5배 느리다.** 매 사이클마다 함수 호출이 더 일어나기 때문이다. 그러면 이 정도 비용으로 시간 정확도를 사는 것이 합당한가? 학습 목적으로는 분명히 그렇다. 상용 게임 호환성용으로는 더더욱 그렇다. 30 MHz 동작 속도는 실제 8비트 시스템(1~8 MHz)을 실시간보다 빠르게 돌리고도 남는다.

> **사이드바: Int vs UByte의 성능 차이는?**
>
> 4장에서 정했던 결정 — "Kotlin/JVM에서 8비트 값은 `Int` + 마스킹으로 표현한다" — 의 정량 근거를 여기서 확인하자. 같은 벤치마크를 `UByte` 버전으로 한 번 더 돌려본다.
>
> | 표현 | Throughput | 상대 비용 |
> |------|------------|-----------|
> | `Int` + `and 0xFF` | ~80M inst/sec | 1.0x (기준) |
> | `UByte` (inline class) | ~72M inst/sec | 1.11x 느림 |
> | `Byte` (signed, 매번 변환) | ~58M inst/sec | 1.38x 느림 |
>
> 어떤가? UByte가 inline class라 거의 비용이 없을 거라는 예상과는 살짝 다르다. **약 10% 정도 차이가 난다.** Kotlin 컴파일러가 inline class를 풀어내지 못하는 자리(예컨대 컬렉션에 담을 때)가 일부 있고, 시프트 연산은 결국 `.toInt()` 변환을 거치기 때문이다. 그래도 10% 정도면 가독성과 타입 안전성의 대가로 충분히 받을 만하다는 의견도 있다. 후반 챕터에서 우리가 UByte로 마이그레이션하지 않은 것은 "성능 때문에"가 아니라 "교육적 일관성 때문에"였다. 비용은 크지 않다.
>
> `Byte`(signed)는 두 자리 수 차이가 난다. 이건 단순한 표현 차이가 아니라 매번 `.toInt() and 0xFF`로 변환을 강요하는 자리에서의 누적 비용이다. **8비트 표현으로 `Byte`를 쓰면 안 된다**는 4장의 결정이 여기서 정량 검증된다.

## "make it work → make it right → make it fast"의 우리 자리

에뮬레이터 개발 커뮤니티에는 한 가지 격언이 있다.

> "Make it work, make it right, make it fast."

"먼저 돌게 만들고, 그 다음 옳게 만들고, 마지막에 빠르게 만들어라." 1989년 Kent Beck이 만든 표현이지만 에뮬레이터 개발에 묘하게 잘 맞는다.

우리 책의 14장까지의 여정을 이 격언에 비춰보자.

- **Make it work:** 1·2장에서 30줄짜리 미니 CPU가 일단 돈다
- **Make it right (1단계):** 3~7장에서 SAP-1이 단계별로 올바르게 동작한다. 어셈블러도 어셈블한 코드가 정확히 실행된다
- **Make it right (2단계):** 8~10장에서 SAP-2의 39개 명령어가 명세대로 동작한다. 디버거가 한 줄씩 짚어준다
- **Make it right (3단계):** 11~13장에서 RISC ISA가 정합성 있게 설계되고 자기 컴파일러가 그 위에서 돈다
- **Make it right (4단계):** 14장에서 cycle-accurate로 시간까지 정확하게 한다

이게 우리 책이 멈추는 자리다. **14장이 "right"의 마지막 단계**다. **"fast"는 우리가 가지 않는 길이다.** 왜?

학습용 시뮬레이터는 빠를 필요가 별로 없다. 우리가 측정한 80M inst/sec은 이미 실제 8080의 400배다. 더 빨리 만들기 위해 JIT 컴파일, 동적 디스패치 제거, 메모리 접근 인라이닝 같은 최적화를 하면 코드가 읽기 어려워진다. **읽기 쉬움이 학습용의 첫 번째 가치**다. 가독성을 포기하면서까지 한 자릿수 배율의 속도를 더 살 이유가 없다.

그러나 만약 자기가 짠 시뮬레이터로 게임을 돌리고 싶다면? 그 자리에서 "fast"의 길이 열린다. JIT 컴파일러를 자기 시뮬레이터에 박아넣을 수도 있고(dynarec), 명령어 디스패치를 jump table로 바꿀 수도 있고, hot path를 inline assembly로 짤 수도 있다. **15장에서 그 길의 청사진을 한 번 더 펴본다.** 

## 실물 빌드 vs 시뮬레이터 — 마지막으로 한 번 더

3장에서 한 번 짚었던 한 가지를 14장 마무리 즈음에서 한 번 더 들여다보자. **실물로 짓는 것과 시뮬레이터로 짓는 것의 차이.**

여러 의견을 옮겨오면 이런 결을 가진다.

> "Tactile experience of cutting wires and physically putting it together creates lasting intuition about hardware behavior — something simulations cannot replicate for embedded systems work." — Hacker News 토론에서

> "$300+ in parts for a computer with only 16 bytes of memory... For learning efficiency, alternatives like nand2tetris offer similar conceptual understanding without physical assembly." — 같은 토론의 다른 입장

두 의견은 어느 쪽도 틀리지 않다. **다른 학습 목적에 다른 답이 맞다.**

이 책의 자리는 명확하다. **"이론 → 시뮬레이터 → 실물"의 3단계 학습 경로에서 가운데 단계.** 1단계(교과서·강의)에서 von Neumann과 fetch-decode-execute 같은 개념을 잡고, 2단계(우리 책)에서 Kotlin으로 손에 잡히게 만들고, 3단계(실물 빌드)에서 floating input, 전압 강하, 타이밍 같은 물리적 변수를 겪어본다.

14장 끝에서 3단계로 가고 싶은 독자에게 추천할 것이 명확하다. **Ben Eater의 YouTube 시리즈.** 이 시리즈는 SAP-1을 74LS 시리즈 IC와 브레드보드로 직접 조립한다. Ben Eater 자체에서 판매하는 8-bit breadboard kit는 약 300달러대(시기에 따라 변동). 풀 시리즈 영상은 약 50~60시간 분량. 디버깅 시간은 그보다 훨씬 많이 든다. 그래도 **"왜 컴퓨터가 동작하는 것이 기적인가"를 손으로 체험하는 데**는 비할 곳이 없다.

자기가 짠 Kotlin SAP-1과 Ben Eater의 브레드보드 SAP-1을 나란히 두고 보자. **같은 SAP-1이다.** 그러나 한쪽은 0과 1의 추상화, 다른 쪽은 5V와 0V의 물리. 14장에서 cycle-accurate로 시간을 더 정확하게 잡았다면, Ben Eater 단계에서는 그 시간이 진짜로 흐르는 것을 본다. LED가 깜빡이고, 클록 발진기가 1Hz로 도는 소리가 들린다. 추상화 두 단계 아래의 세계가 거기 있다.

급할 것 없다. 14장이 끝나는 자리에서 잠깐 멈춰, 자기가 만든 것이 어디 있는지를 손에 쥐어보자. 1단계와 3단계 사이의 가운데 단계 — 그 자리가 가장 풍부하다. 추상과 물리 둘 다와 손을 잡을 수 있는 자리다.

> **GitHub 산출물**
>
> ```
> chapter-14/
>   build.gradle.kts                       ← JMH 의존성 추가
>   src/main/kotlin/risc8/
>     CycleAccurate.kt                     ← cycle-accurate SAP-2/RISC-8 코어
>     MicroStep.kt                         ← 마이크로코드 표 (10장에서 가져와 재해석)
>     PeripheralBus.kt                     ← 가상 PPU/타이머/UART의 공유 클록
>   src/test/kotlin/risc8/
>     CycleAccurateRegressionTest.kt       ← 39개 명령어 사이클 회귀
>     InterruptLatencyTest.kt              ← IRQ 응답 시점 검증
>   src/jmh/kotlin/risc8/
>     CpuBenchmark.kt                      ← throughput 측정
>     ByteRepresentationBenchmark.kt       ← Int vs UByte vs Byte 비교
> ```
>
> 실행:
> ```
> ./gradlew :chapter-14:test           # 정확도 회귀
> ./gradlew :chapter-14:jmh             # 성능 벤치마크
> ```
>
> JMH 결과는 자기 환경에서 다르게 나올 수 있다. CPU·JVM 버전·창문 열어둔 정도(농담)에 따라 변한다. **상대 비율**(cycle-accurate vs instruction-accurate, Int vs UByte)이 더 안정적이다.

## 마무리 — 정확도라는 단어의 두께

다시 정리하자.

1. **정확도의 세 등급** — instruction-accurate, cycle-accurate, sub-cycle-accurate — 을 손에 쥐었다. 우리 SAP-2는 1단계에서 2단계로 한 칸 올라갔다
2. **마리오가 깨지는 이유**를 봤다 — PPU/CPU의 사이클 동기. 그래픽 동기는 cycle-accurate의 한 결과
3. **cycle-accurate의 진짜 동기는 인터럽트 타이밍** — IRQ가 명령어 한 가운데에 들어왔을 때의 latency가 결정적
4. **SAP-2를 cycle-accurate로 리팩토링**했다 — `step()`이 한 명령어에서 한 사이클로. 마이크로코드 표가 시간 모델 그 자체가 된다
5. **39개 명령어 사이클 회귀 테스트**로 검증 — instruction 결과 정확도는 유지하면서 시간 정확도를 더했다
6. **ksim65의 cycle-exact 포기**가 부끄러운 일이 아니다 — 목적에 맞는 정확도 등급의 선택
7. **JMH로 성능을 측정**했다 — instruction-accurate ~80M inst/sec, cycle-accurate ~30M cycles/sec, UByte는 약 10% 느림
8. **"make it work → right → fast"** 격언에서 우리 책은 "right"의 마지막에서 멈춘다 — "fast"는 가독성 비용이 너무 크다
9. **실물 빌드(Ben Eater)는 3단계 학습의 마지막** — 14장 끝에서 자연스럽게 안내

여기까지 따라온 독자에게는 8비트 CPU 짓기의 거의 전 과정이 손에 있다. SAP-1·SAP-2·8비트 RISC 시뮬레이터, 어셈블러·디스어셈블러·디버거, 테스트 ROM, 그리고 이제 cycle-accurate 리팩토링까지. **남은 한 칸은 "여기서 어디로?"다.** 15장에서 그 다음 12개월의 청사진을 펴낸다. CPU 다음의 컴퓨터 — 메모리 시스템, I/O 디바이스, 인터럽트 컨트롤러, 그리고 결국 운영체제까지. 자기가 짠 작은 8비트 CPU가 자기 컴퓨터 전체로 가는 다리가 어디 있는지를 한 챕터로 묶는다.

잠깐 쉬어가자. 차 한 잔 들고 자기 SAP-2를 cycle-accurate로 한 번 더 돌려보자. JMH가 워밍업 한 번 더 돌고 throughput 숫자를 뽑아내는 그 짧은 순간에, 자기가 지난 13개 챕터에 걸쳐 무엇을 만들었는지를 다시 짚어보자. 15장에서 만나자. 마지막 챕터다.
