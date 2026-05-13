package sap.ch04

sealed class Instruction(val opcode: Int) {
    data class Lda(val address: Int) : Instruction(0x0)
    data class Add(val address: Int) : Instruction(0x1)
    data class Sub(val address: Int) : Instruction(0x2)
    data object Out : Instruction(0xE)
    data object Hlt : Instruction(0xF)

    companion object {
        fun decode(byte: Int): Instruction {
            val op = (byte shr 4) and 0xF
            val addr = byte and 0xF
            return when (op) {
                0x0 -> Lda(addr)
                0x1 -> Add(addr)
                0x2 -> Sub(addr)
                0xE -> Out
                0xF -> Hlt
                else -> error("Unknown opcode: 0x${op.toString(16)}")
            }
        }
    }

    fun encode(): Int = when (this) {
        is Lda -> (0x0 shl 4) or (address and 0xF)
        is Add -> (0x1 shl 4) or (address and 0xF)
        is Sub -> (0x2 shl 4) or (address and 0xF)
        is Out -> (0xE shl 4)
        is Hlt -> (0xF shl 4)
    }
}
