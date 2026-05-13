package sap.ch02

class MiniCpu(private val memory: IntArray) {
    var pc: Int = 0
        private set
    var accumulator: Int = 0
        private set
    var halted: Boolean = false
        private set

    companion object {
        const val OP_ADD = 0x01
        const val OP_HLT = 0x10
    }

    fun run() {
        while (!halted && pc < memory.size) {
            val opcode = fetch()
            when (opcode) {
                OP_ADD -> {
                    if (pc < memory.size) {
                        val addr = fetch()
                        if (addr in memory.indices) {
                            accumulator = (accumulator + memory[addr]) and 0xFF
                        }
                    } else {
                        halted = true
                    }
                }
                OP_HLT -> halted = true
                else -> halted = true
            }
        }
        if (!halted) halted = true
    }

    private fun fetch(): Int = memory[pc++]
}

fun main() {
    // 메모리 레이아웃:
    //   [0] ADD addr=5  →  A += memory[5] = 17
    //   [2] ADD addr=6  →  A += memory[6] = 25
    //   [4] HLT
    //   [5] 17  (데이터)
    //   [6] 25  (데이터)
    val program = intArrayOf(0x01, 5, 0x01, 6, 0x10, 17, 25)
    val cpu = MiniCpu(program)
    cpu.run()
    println("Accumulator = ${cpu.accumulator}")   // 출력: Accumulator = 42
}
