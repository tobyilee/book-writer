package risc8.ch14

/**
 * RISC-8 cycle-accurate 시뮬레이터.
 *
 * 13장의 [Cpu]는 instruction-accurate — 어떤 명령어든 1 step에 끝난다. 본 클래스는 그 위에
 * "명령어별 진짜 사이클 비용"을 누적하는 얇은 wrapper다. 의미적인 결과(register/memory)는 13장
 * 시뮬레이터와 동일하지만, [cycleCount]가 다르다.
 *
 * 사이클 비용 모델 (RISC-8용으로 간소화한 단일-이슈 in-order 파이프라인 가정):
 *
 * | 명령어 그룹 | cycle |
 * |-------------|-------|
 * | 산술/논리 R-type, ADDI/ANDI, LI | 1 |
 * | LB/SB (메모리 접근 stall) | 2 |
 * | BEQ/BNE — taken (파이프라인 flush) | 2 |
 * | BEQ/BNE — not taken | 1 |
 * | JAL/JR | 2 |
 * | NOP/ECALL/EBREAK/HALT | 1 |
 *
 * 즉, 보통 명령어 1개 = 1 cycle이지만 메모리 접근·점프·잡힌 분기는 +1 cycle씩 더 든다.
 * 진짜 5-stage 파이프라인의 분기 예측 실패 패널티·load-use hazard를 본뜬 최소 모델이다.
 */
class CycleAccurateCpu(program: IntArray, memorySize: Int = 256) {
    private val cpu = Cpu(program, memorySize)

    /** 누적 사이클 카운트 — instruction-accurate Cpu의 [Cpu.cyclesExecuted]와 다르다. */
    var cycleCount: Long = 0L
        private set

    val instructions: IntArray get() = cpu.instructions
    val registers: IntArray get() = cpu.registers
    val memory: IntArray get() = cpu.memory
    val pc: Int get() = cpu.pc
    val halted: Boolean get() = cpu.halted

    fun reset() {
        cpu.reset()
        cycleCount = 0L
    }

    fun step() {
        if (cpu.halted) return
        val pcBefore = cpu.pc
        val word = if (pcBefore in cpu.instructions.indices) cpu.instructions[pcBefore] else 0
        val instr = Instruction.decode(word)
        // 분기는 step() 전에 레지스터 상태를 보고 taken 여부를 미리 판정한다 —
        // step() 후 PC만 보면 offset=0인 self-branch를 구분 못한다.
        val taken = when (instr) {
            is Instruction.Beq -> cpu.registers[instr.rd] == cpu.registers[instr.rs1]
            is Instruction.Bne -> cpu.registers[instr.rd] != cpu.registers[instr.rs1]
            else -> false
        }
        cpu.step()
        cycleCount += cyclesFor(instr, taken)
    }

    /** maxCycles 동안 또는 HALT까지 실행. */
    fun run(maxCycles: Long = 100_000L) {
        while (!cpu.halted && cycleCount < maxCycles) step()
    }

    private fun cyclesFor(instr: Instruction, takenBranch: Boolean): Int = when (instr) {
        is Instruction.Lb, is Instruction.Sb -> 2
        is Instruction.Beq, is Instruction.Bne -> if (takenBranch) 2 else 1
        is Instruction.Jal, is Instruction.Jr -> 2
        else -> 1
    }
}
