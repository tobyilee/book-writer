# 10장 — 마이크로코드와 디버거: CPU를 한 사이클씩 들여다보자

## 핵심 질문

- "컨트롤러가 ROM이 된다"는 게 대체 무슨 뜻인가? 지금까지 만든 하드와이어드 컨트롤러와 무엇이 다른가?
- 내 CPU의 내부를 어떻게 한 클럭씩, 한 명령씩 들여다볼 수 있을까? 실제 칩의 ICE나 gdb는 무엇을 하고 있는 걸까?
- 회귀 테스트라는 게 그냥 단위 테스트가 아니다 — "test ROM"이라는 오래된 관습이 따로 있다. 그건 왜 따로 존재하나?

이 챕터에서 우리는 두 가지를 만든다. 첫째, SAP-1의 컨트롤러를 마이크로코드 ROM 테이블로 재구성한다(하드와이어드 → 마이크로프로그래밍 전환). 둘째, SAP-2를 위한 디버거를 만들고 인터랙티브 CLI를 붙인다. 마지막으로 ISA의 결정적인 종료 상태를 검증하는 test ROM 한 묶음을 두고, 앞으로 CPU 내부를 바꿔도 외부 동작이 흔들리지 않게 한다.

---

## 하드와이어드에서 마이크로코드로

5장의 SAP-1 컨트롤러는 디코더와 카운터를 게이트로 엮어 매 T-state마다 어떤 제어선을 띄울지 결정했다. opcode가 4비트, T-state가 6단계니까 24개 조합이고, 그 조합 각각에 12개 제어선 중 어떤 게 HIGH가 되어야 하는지가 회로로 박혀 있었다. 이걸 **하드와이어드 컨트롤(hardwired control)**이라 부른다 — 빠르지만, 명령어를 추가하거나 마이크로 시퀀스를 바꾸려면 회로를 다시 만들어야 한다.

마이크로프로그래밍은 그 회로를 **ROM**으로 옮긴 것이다. opcode와 T-state를 주소로 묶어 ROM에 던지면, 그 주소의 ROM 워드가 곧 "이번 사이클에 띄울 제어선들의 비트맵"이 된다. 회로는 ROM 주소 디코더와 워드 출력만 갖추면 되고, 명령어를 추가하는 일은 ROM의 다음 슬롯을 채우는 일이 된다. 마이크로 시퀀스를 다시 짜고 싶으면 ROM만 다시 굽는다.

IBM System/360, VAX, x86은 모두 마이크로코드를 깊이 쓴다. 반대로 RISC 철학(SPARC, 초기 MIPS·ARM)은 "마이크로코드 없이 명령어가 한 사이클에 끝나도록 ISA를 짜자"는 입장이었다 — 그래서 RISC라는 이름이 붙었다. 8080도 사실 마이크로코드 칩이고, 6502는 PLA(programmable logic array) 기반의 거의-마이크로코드라고 부른다. 어느 쪽이든 핵심은 "제어 신호의 시퀀스를 표(table)로 만들어 두면 ISA 진화가 쉬워진다"는 것이다.

---

## SAP-1 마이크로코드 ROM

본 책의 SAP-1은 5개 명령어(LDA, ADD, SUB, OUT, HLT)에 6개 T-state, 13개 제어 신호를 쓴다. 매트릭스 크기는 (5 + 1 fetch) × 6 = 36개 슬롯이지만 fetch 3개는 모든 명령어가 공유하니까 실제 ROM 워드 수는 (5 × 3) + 3 = 18 정도다. 본 책에서는 Kotlin enum과 lookup 함수로 그 매트릭스를 재현한다.

```kotlin
enum class MicroSignal {
    PC_OUT, MAR_LOAD, MEM_OUT, IR_LOAD,
    IR_OUT, A_LOAD, A_OUT,
    B_LOAD, ALU_OUT, ALU_SUB_MODE,
    OUT_LOAD, PC_INC, HALT,
}

object MicroRom {
    fun signalsFor(opcode: Int, tState: Int): Set<MicroSignal> {
        when (tState) {
            1 -> return setOf(PC_OUT, MAR_LOAD)
            2 -> return setOf(PC_INC)
            3 -> return setOf(MEM_OUT, IR_LOAD)
        }
        val op = (opcode shr 4) and 0xF
        return when (op) {
            0x0 -> when (tState) { /* LDA T4, T5 */ }
            0x1 -> when (tState) { /* ADD T4, T5, T6 */ }
            0x2 -> when (tState) { /* SUB T4, T5, T6 (+ ALU_SUB_MODE) */ }
            0xE -> when (tState) { /* OUT T4 */ }
            0xF -> when (tState) { /* HLT T4 */ }
            else -> emptySet()
        }
    }
}
```

호출자는 (IR 안의 opcode, 현재 T-state)를 던지고, 활성 마이크로 신호의 집합을 받는다. 실제 하드웨어에서는 그 집합의 원소들이 한 클럭 사이클 동안 동시에 HIGH가 된다.

> **`ControlSignal` vs `MicroSignal`** — 같은 SAP-1을 두 시각에서 보고 있다. ch05의 `Controller`는 하드와이어드 시퀀서(`ControlSignal`)이고, 이번 챕터의 `MicroRom`은 ROM-lookup 컨트롤러(`MicroSignal`)다. 신호 세트도 살짝 다르다 — 하드와이어드는 ALU 동작을 `ALU_ADD`·`ALU_SUB`로 명시했지만, 마이크로코드 쪽은 ALU 출력(`ALU_OUT`)을 띄우고 모드 비트(`ALU_SUB_MODE`)를 별도로 둔다(실제 ROM은 워드 비트를 그렇게 나눈다). 둘 다 같은 SAP-1을 돌릴 수 있다 — 동등성 검증은 14장의 cycle-accurate 시뮬레이터에서 본격적으로 한다.

> **왜 Map이 아니라 `when`인가?** 36개짜리 매트릭스를 `Map<Pair<Int,Int>, Set<ControlSignal>>`로도 만들 수 있다. 가독성은 비슷하다. 다만 `when`은 "ROM 어드레스 디코더"의 시각적 은유를 더 잘 살린다고 봤다 — 진짜 ROM도 결국 "주소를 받고 워드를 뱉는 함수"이므로.

---

## 디버거 — CPU 안을 들여다보기

CPU를 만들었으면 그 안을 들여다보고 싶은 건 자연스러운 욕구다. 실제 칩 개발자는 ICE(In-Circuit Emulator)를 쓰고, 우리 같은 소프트웨어 개발자는 gdb를 쓴다. 둘 다 본질적으로 같은 일을 한다.

1. **Step** — 한 명령씩 진행하고 멈춘다.
2. **Continue** — 다음 breakpoint나 HLT까지 자유롭게 달린다.
3. **Breakpoint** — 특정 PC에 도달하면 멈춘다.
4. **Inspect** — 레지스터와 메모리를 들여다본다.

본 책의 `Debugger`는 SAP-2 위에 얹는 외부 어댑터다. CPU 자체는 건드리지 않고 `cpu.step()`을 감싸기만 한다.

```kotlin
class Debugger(private val cpu: Sap2) {
    private val breakpoints = mutableSetOf<Int>()
    private var hitBreakpoint: Int? = null

    fun continueUntilBreakOrHalt(maxSteps: Int = 1_000_000) {
        hitBreakpoint = null
        var steps = 0
        while (!cpu.core.halted && steps < maxSteps) {
            cpu.step()
            steps++
            if (cpu.core.pc in breakpoints) {
                hitBreakpoint = cpu.core.pc
                return
            }
        }
    }
}
```

여기서 breakpoint의 의미가 미묘하다. `step()` 직후 PC를 확인하니까, breakpoint는 "그 주소의 명령이 실행되기 직전"에 잡힌다. 실제 gdb도 똑같다 — `break main`은 main의 첫 명령을 실행하기 전에 멈춘다. 이 의미를 테스트로 못 박아 둔다.

```kotlin
it("breakpoint에서 정지 — 그 명령은 아직 실행되지 않은 상태") {
    val (cpu, dbg) = setup()  // LDI A,5; INC A; INC A; HLT
    dbg.setBreakpoint(0x02)   // 첫 INC A 위치
    dbg.continueUntilBreakOrHalt()
    cpu.core.pc shouldBe 0x02
    cpu.regs.A.value shouldBe 5  // LDI만 실행되고 INC는 아직 안 함
}
```

---

## DebuggerCli — REPL 한 페이지

`DebuggerCli`는 stdin에서 명령을 받아 `Debugger`를 운전한다.

```
$ ./gradlew :chapter-10:run --quiet
SAP-2 디버거 — 명령: s(tep) c(ontinue) b <addr> r(egisters) m <addr> q(uit)
PC=0x0000  A=0x00 B=0x00 C=0x00  SP=0xFFFE  Z=0  HALT=false
> s
PC=0x0002  A=0x48 B=0x00 C=0x00  SP=0xFFFE  Z=0  HALT=false
> b 0x000A
Breakpoint set at 0xA
> c
Breakpoint at 0xA
PC=0x000A  A=0x65 B=0x00 C=0x00  SP=0xFFFE  Z=0  HALT=false
> q
Goodbye
```

명령은 한 글자 + 옵션이다. `b 0x000A` 또는 `b $A` 또는 `b 10` — 진수 표기 셋 다 받는다.

> **인터랙티브 CLI라 단위 테스트는?** stdin을 추상화하면 테스트는 가능하지만, 본 책의 이 챕터에서는 `Debugger` 자체를 단위 테스트하고 CLI는 thin wrapper로 둔다. CLI를 직접 돌리는 건 독자 몫이다 — `./gradlew :chapter-10:run`으로 띄우고, `q`로 빠져나오자.

---

## Test ROM — 회귀 테스트의 오래된 관습

CPU 개발에서 "test ROM"이라는 단어는 특별한 무게가 있다. 6502 커뮤니티에는 [Klaus Dormann의 6502 functional test](https://github.com/Klaus2m5/6502_65C02_functional_tests)라는 ROM이 돌아다닌다 — 거의 모든 명령어 조합을 결정적인 종료 상태로 몰아넣는 어셈블리 프로그램이다. 어떤 에뮬레이터든 그 ROM을 통과하면 "6502를 흉내냈다"고 자처할 수 있다.

본 책의 SAP-2에도 같은 정신으로 test ROM을 둔다. 단, 6502 functional test의 축소판이다.

| ROM | 검증 항목 | 종료 상태 |
|---|---|---|
| 산술 ROM | `LDI / ADD / DEC` | `A = 7`, `Z = false` |
| 분기 ROM | `LDI / DEC / JNZ` 카운터 루프 | `A = 0`, `Z = true` |
| CALL/RET ROM | 서브루틴이 A에 10을 더함 | `A = 15` |

```kotlin
it("분기 ROM: counter loop, A=0 종료") {
    val cpu = Sap2()
    // LDI A, 3; loop: DEC A; JNZ loop; HLT
    cpu.loadProgram(intArrayOf(0x01, 3, 0x33, 0x42, 0x02, 0x00, 0xFF))
    cpu.run()
    cpu.regs.A.value shouldBe 0
    cpu.zeroFlag shouldBe true
}
```

내부 구조를 바꿔도 이 ROM들이 통과하면 외부 동작은 그대로다 — 그게 회귀 테스트의 약속이다. 12장에서 인터럽트를 넣고, 13장에서 파이프라인을 깎아도, 이 ROM들은 계속 통과해야 한다. 통과하지 못한다면 ISA가 바뀐 거고, 그건 의도된 일이어야 한다.

---

## 실행

```
./gradlew :chapter-10:test         # 전체 테스트
./gradlew :chapter-10:run          # DebuggerCli 진입 (q로 종료)
```

---

## 테스트

| 테스트 클래스 | 검증 항목 |
|---|---|
| `MicroRomTest` | Fetch T1~T3 / LDA / ADD / SUB(SUB_MODE) / OUT / HLT의 control signal 매트릭스 |
| `DebuggerTest` | step·continue·breakpoint·clearBreakpoint·registerDump·memoryDump |
| `Sap2TestRomSpec` | 산술 / 분기 / CALL-RET test ROM 회귀 검증 |
| (ch09 이관) | Sap2Hello, Sap2Fib, Sap2Instructions, Sap2Core, RegisterFile, AluFlags, ProgramCounter, Register, Clock, Instruction, Assembler, Lexer, SAP-1 통합 |

---

## 산출물

```
chapter-10/
├── build.gradle.kts
├── src/
│   ├── main/
│   │   ├── kotlin/sap/ch10/
│   │   │   ├── MicroRom.kt           ← 신규: SAP-1 마이크로코드 ROM 테이블
│   │   │   ├── Debugger.kt           ← 신규: breakpoint·step·dump
│   │   │   ├── DebuggerCli.kt        ← 신규: REPL CLI
│   │   │   ├── Sap2.kt               ← ch09 이관 (디버거 대상)
│   │   │   └── (Sap1·Sap2Core·RegisterFile·Register·AluFlags·Bus·Clock·Controller·Instruction·ProgramCounter·Ram·Sap2Util — ch09 이관)
│   │   │   └── asm/
│   │   │       └── (Sap2Assembler·Assembler·Disassembler·Lexer — ch09 이관)
│   │   └── resources/programs/       ← hello.sap2·fib.sap2·add.sap1 (ch09 이관)
│   └── test/kotlin/sap/ch10/
│       ├── MicroRomTest.kt           ← 신규
│       ├── DebuggerTest.kt           ← 신규
│       ├── Sap2TestRomSpec.kt        ← 신규
│       └── (ch09 이관 — Sap2HelloTest, Sap2FibTest, Sap2InstructionsTest, …)
```
