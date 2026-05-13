package risc8.ch13

/**
 * RISC-8 instruction-accurate 시뮬레이터.
 *
 * - 8개 8-bit 범용 레지스터 (R0은 항상 0; 쓰기 무시).
 * - 16-bit PC, instruction은 별도 IntArray (Harvard-ish).
 * - 8-bit data memory, 기본 256 바이트.
 * - PC는 명령어당 +1 (워드 단위 저장이라 +2 아님).
 */
class Cpu(program: IntArray, val memorySize: Int = 256) {
    val instructions: IntArray = program.copyOf()
    val registers: IntArray = IntArray(8)
    val memory: IntArray = IntArray(memorySize)

    var pc: Int = 0
        private set
    var halted: Boolean = false
        private set
    var cyclesExecuted: Int = 0
        private set

    fun reset() {
        registers.fill(0)
        memory.fill(0)
        pc = 0
        halted = false
        cyclesExecuted = 0
    }

    /** maxCycles 동안 또는 HALT까지 실행. */
    fun run(maxCycles: Int = 1_000_000) {
        var c = 0
        while (!halted && c < maxCycles) {
            step()
            c++
        }
    }

    fun step() {
        if (halted) return
        if (pc !in instructions.indices) {
            halted = true
            return
        }
        val word = instructions[pc]
        pc++
        val instr = Instruction.decode(word)
        execute(instr)
        registers[0] = 0  // R0은 매 사이클 끝에 0으로 강제 (관습대로).
        cyclesExecuted++
    }

    private fun execute(instr: Instruction) {
        when (instr) {
            is Instruction.Nop -> Unit
            is Instruction.Add -> registers[instr.rd] = (registers[instr.rs1] + registers[instr.rs2]) and 0xFF
            is Instruction.Sub -> registers[instr.rd] = (registers[instr.rs1] - registers[instr.rs2]) and 0xFF
            is Instruction.And -> registers[instr.rd] = (registers[instr.rs1] and registers[instr.rs2]) and 0xFF
            is Instruction.Or -> registers[instr.rd] = (registers[instr.rs1] or registers[instr.rs2]) and 0xFF
            is Instruction.Xor -> registers[instr.rd] = (registers[instr.rs1] xor registers[instr.rs2]) and 0xFF
            is Instruction.Shl ->
                registers[instr.rd] = (registers[instr.rs1] shl (registers[instr.rs2] and 7)) and 0xFF
            is Instruction.Shr ->
                registers[instr.rd] = ((registers[instr.rs1] and 0xFF) ushr (registers[instr.rs2] and 7)) and 0xFF
            is Instruction.AddI -> registers[instr.rd] = (registers[instr.rs1] + instr.imm) and 0xFF
            is Instruction.AndI -> registers[instr.rd] = (registers[instr.rs1] and (instr.imm and 0xFF)) and 0xFF
            is Instruction.Lb -> {
                val addr = (registers[instr.rs1] + instr.imm) and 0xFF
                registers[instr.rd] = memory[addr % memorySize] and 0xFF
            }
            is Instruction.Sb -> {
                val addr = (registers[instr.rs1] + instr.imm) and 0xFF
                memory[addr % memorySize] = registers[instr.rd] and 0xFF
            }
            is Instruction.Beq ->
                if (registers[instr.rd] == registers[instr.rs1]) pc = (pc + instr.off) and 0xFFFF
            is Instruction.Bne ->
                if (registers[instr.rd] != registers[instr.rs1]) pc = (pc + instr.off) and 0xFFFF
            is Instruction.Jal -> {
                if (instr.rd != 0) registers[instr.rd] = pc and 0xFF  // 복귀 주소 (8-bit truncated)
                pc = (pc + instr.imm6) and 0xFFFF
            }
            is Instruction.Jr -> pc = (registers[instr.rs1] + instr.imm) and 0xFFFF
            is Instruction.Li -> registers[instr.rd] = instr.imm6 and 0xFF
            is Instruction.Ecall -> halted = true   // 본 책에서는 단순 종료로 처리.
            is Instruction.Ebreak -> halted = true
            is Instruction.Halt -> halted = true
        }
    }
}
