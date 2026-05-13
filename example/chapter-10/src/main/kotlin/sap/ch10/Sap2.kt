package sap.ch10

/**
 * SAP-2 실행기. ch08의 Sap2Core(64KB RAM + 16비트 PC)와 RegisterFile(A,B,C) 위에
 * 분기·서브루틴·I/O 명령어를 얹은 단순화된 8080-style ISA를 실행한다.
 *
 * 본 책의 SAP-2 ISA subset:
 * - 즉값 로드: LDI A/B/C, imm8           (0x01..0x03)
 * - 레지스터 이동: MOV A,B / A,C / B,A / C,A / B,C / C,B  (0x10..0x15)
 * - 산술: ADD B, ADD C, SUB B            (0x20..0x22)
 * - 증감: INC A, INC B, INC C, DEC A, DEC C  (0x30..0x34)
 * - 분기: JMP, JZ, JNZ addr16            (0x40..0x42)
 * - 서브루틴: CALL addr16, RET           (0x50, 0x51)
 * - I/O: IN port, OUT port (4비트 포트)  (0x60, 0x61)
 * - HLT                                  (0xFF)
 *
 * 플래그: Z(zero)는 ADD/SUB/INC/DEC 결과로 갱신된다.
 * 스택: 16비트 SP가 0xFFFE에서 시작하고 push 시 2바이트 감소.
 */
class Sap2 {
    val core = Sap2Core()
    val regs = RegisterFile()

    var sp: Int = 0xFFFE
        private set

    var zeroFlag: Boolean = false
        private set

    private val inputPorts = IntArray(16)
    val outputPorts: IntArray = IntArray(16)
    private val outputBuf = StringBuilder()
    private val port0History = mutableListOf<Int>()

    /** 포트 0에 출력된 바이트를 문자열로 누적한 것. ASCII 스트림 용. */
    val port0Output: String get() = outputBuf.toString()

    /** 포트 0에 출력된 바이트의 정수 시퀀스(숫자 출력 검사용). */
    val port0OutputBytes: List<Int> get() = port0History.toList()

    fun setInputPort(port: Int, value: Int) {
        inputPorts[port and 0xF] = value and 0xFF
    }

    fun loadProgram(bytes: IntArray, base: Int = 0) {
        for ((i, b) in bytes.withIndex()) core.writeByte(base + i, b)
        core.setPc(base)
    }

    fun run(maxSteps: Int = 1_000_000) {
        var steps = 0
        while (!core.halted && steps < maxSteps) {
            step()
            steps++
        }
        check(core.halted) { "max steps exceeded — likely infinite loop (steps=$steps)" }
    }

    fun step() {
        if (core.halted) return
        val opPc = core.pc
        val op = core.fetch()
        when (op) {
            0x00 -> {} // NOP
            0x01 -> regs.A.load(core.fetch())
            0x02 -> regs.B.load(core.fetch())
            0x03 -> regs.C.load(core.fetch())
            0x10 -> regs.A.load(regs.B.value)
            0x11 -> regs.A.load(regs.C.value)
            0x12 -> regs.B.load(regs.A.value)
            0x13 -> regs.C.load(regs.A.value)
            0x14 -> regs.B.load(regs.C.value)
            0x15 -> regs.C.load(regs.B.value)
            0x20 -> { val r = (regs.A.value + regs.B.value) and 0xFF; regs.A.load(r); zeroFlag = r == 0 }
            0x21 -> { val r = (regs.A.value + regs.C.value) and 0xFF; regs.A.load(r); zeroFlag = r == 0 }
            0x22 -> { val r = (regs.A.value - regs.B.value) and 0xFF; regs.A.load(r); zeroFlag = r == 0 }
            0x30 -> { val r = (regs.A.value + 1) and 0xFF; regs.A.load(r); zeroFlag = r == 0 }
            0x31 -> { val r = (regs.B.value + 1) and 0xFF; regs.B.load(r); zeroFlag = r == 0 }
            0x32 -> { val r = (regs.C.value + 1) and 0xFF; regs.C.load(r); zeroFlag = r == 0 }
            0x33 -> { val r = (regs.A.value - 1) and 0xFF; regs.A.load(r); zeroFlag = r == 0 }
            0x34 -> { val r = (regs.C.value - 1) and 0xFF; regs.C.load(r); zeroFlag = r == 0 }
            0x40 -> core.setPc(fetch16())
            0x41 -> { val a = fetch16(); if (zeroFlag) core.setPc(a) }
            0x42 -> { val a = fetch16(); if (!zeroFlag) core.setPc(a) }
            0x50 -> {
                val addr = fetch16()
                val retAddr = core.pc
                // SP를 가리키는 바이트(low), SP-1을 가리키는 바이트(high)에 저장
                core.writeByte(sp, retAddr and 0xFF)
                core.writeByte((sp - 1) and 0xFFFF, (retAddr shr 8) and 0xFF)
                sp = (sp - 2) and 0xFFFF
                core.setPc(addr)
            }
            0x51 -> {
                sp = (sp + 2) and 0xFFFF
                val hi = core.readByte((sp - 1) and 0xFFFF)
                val lo = core.readByte(sp)
                core.setPc((hi shl 8) or lo)
            }
            0x60 -> {
                val port = core.fetch() and 0xF
                regs.A.load(inputPorts[port])
            }
            0x61 -> {
                val port = core.fetch() and 0xF
                val value = regs.A.value
                outputPorts[port] = value
                if (port == 0) {
                    outputBuf.append(value.toChar())
                    port0History.add(value)
                }
            }
            0xFF -> core.halt()
            else -> error(
                "Unknown SAP-2 opcode: 0x${op.toString(16).padStart(2, '0').uppercase()} " +
                    "at PC=0x${opPc.toString(16).padStart(4, '0').uppercase()}"
            )
        }
    }

    private fun fetch16(): Int {
        val lo = core.fetch()
        val hi = core.fetch()
        return (hi shl 8) or lo
    }
}
