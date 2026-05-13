package sap.ch10

/**
 * SAP-1 통합 시뮬레이터 (instruction-accurate).
 *
 * 분리되어 있던 ALU·Register·PC·RAM 을 한 클래스 안에 묶고,
 * fetch → decode → execute 를 한 step() 안에서 모두 끝낸다.
 *
 * T-state 6사이클(W-bus 위에서 tri-state로 신호가 흐르는 모양)은
 * 14장(cycle-accurate)에서 본격적으로 다룬다. 본 챕터는
 * "분리된 모듈이 합쳐서 첫 프로그램을 돌리는 순간"에 집중한다.
 */
class Sap1(rom: IntArray) {
    val ram: Ram = Ram(rom)
    val a: Register = Register()
    val b: Register = Register()
    val outReg: Register = Register()
    val pc: ProgramCounter = ProgramCounter()

    var halted: Boolean = false
        private set
    var output: Int = 0
        private set
    var cyclesExecuted: Int = 0
        private set

    fun run() {
        while (!halted) step()
    }

    fun step() {
        if (halted) return
        val byte = ram.read(pc.value)
        pc.increment()
        val instr = Instruction.decode(byte)
        execute(instr)
        cyclesExecuted++
    }

    private fun execute(instr: Instruction) {
        when (instr) {
            is Instruction.Lda -> a.load(ram.read(instr.address))
            is Instruction.Add -> {
                b.load(ram.read(instr.address))
                a.load(AluFlags.add(a.value, b.value).value)
            }
            is Instruction.Sub -> {
                b.load(ram.read(instr.address))
                a.load(AluFlags.sub(a.value, b.value).value)
            }
            is Instruction.Out -> {
                outReg.load(a.value)
                output = a.value
            }
            is Instruction.Hlt -> halted = true
        }
    }
}
