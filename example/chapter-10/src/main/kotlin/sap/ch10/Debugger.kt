package sap.ch10

/**
 * SAP-2용 인터랙티브 디버거.
 *
 * 실제 칩의 ICE(In-Circuit Emulator)나 gdb의 축소판이다 — breakpoint를 세팅하고,
 * 한 명령씩 step하고, 레지스터/메모리를 들여다본다.
 * CPU 자체는 건드리지 않고 외곽에서 step()을 감싸기만 한다.
 */
class Debugger(private val cpu: Sap2) {
    private val breakpoints = mutableSetOf<Int>()
    private var hitBreakpoint: Int? = null

    fun setBreakpoint(addr: Int) { breakpoints.add(addr and 0xFFFF) }
    fun clearBreakpoint(addr: Int) { breakpoints.remove(addr and 0xFFFF) }
    fun listBreakpoints(): List<Int> = breakpoints.toList().sorted()

    /** 한 명령 실행하고 그 결과 PC가 breakpoint면 표시만 남긴다(이미 진행한 step은 되돌리지 않는다). */
    fun step() {
        cpu.step()
        if (cpu.core.pc in breakpoints) hitBreakpoint = cpu.core.pc
    }

    /**
     * Breakpoint를 만나거나 HLT까지 진행한다.
     * step 직후 PC가 breakpoint 주소면 멈춘다 — 즉 breakpoint는 "그 주소의 명령을 실행하기 직전"에 잡힌다.
     */
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

    val lastBreakpoint: Int? get() = hitBreakpoint
    val pc: Int get() = cpu.core.pc
    val halted: Boolean get() = cpu.core.halted

    fun registerDump(): String = buildString {
        append("PC=0x${cpu.core.pc.toString(16).padStart(4, '0').uppercase()}  ")
        append("A=0x${cpu.regs.A.value.toString(16).padStart(2, '0').uppercase()} ")
        append("B=0x${cpu.regs.B.value.toString(16).padStart(2, '0').uppercase()} ")
        append("C=0x${cpu.regs.C.value.toString(16).padStart(2, '0').uppercase()}  ")
        append("SP=0x${cpu.sp.toString(16).padStart(4, '0').uppercase()}  ")
        append("Z=${if (cpu.zeroFlag) 1 else 0}  ")
        append("HALT=${cpu.core.halted}")
    }

    fun memoryDump(start: Int, length: Int = 16): String = buildString {
        var i = 0
        while (i < length) {
            val rowAddr = (start + i) and 0xFFFF
            append("0x${rowAddr.toString(16).padStart(4, '0').uppercase()}: ")
            var j = 0
            while (j < 16 && i + j < length) {
                val byte = cpu.core.readByte((start + i + j) and 0xFFFF)
                append("${byte.toString(16).padStart(2, '0').uppercase()} ")
                j++
            }
            append("\n")
            i += 16
        }
    }
}
