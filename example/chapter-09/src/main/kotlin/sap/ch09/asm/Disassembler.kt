package sap.ch09.asm

import sap.ch09.Instruction

object Disassembler {
    fun bytesToText(bytes: IntArray): String {
        val sb = StringBuilder()
        for ((i, byte) in bytes.withIndex()) {
            sb.append("$${i.toString(16).padStart(2, '0').uppercase()}: ")
            sb.append("0x${byte.toString(16).padStart(2, '0').uppercase()}  ")
            try {
                val instr = Instruction.decode(byte)
                sb.append(formatInstr(instr))
            } catch (e: Exception) {
                sb.append("$${byte.toString(16).uppercase()}")
            }
            sb.append("\n")
        }
        return sb.toString()
    }

    private fun formatInstr(instr: Instruction): String = when (instr) {
        is Instruction.Lda -> "LDA \$${instr.address.toString(16).uppercase()}"
        is Instruction.Add -> "ADD \$${instr.address.toString(16).uppercase()}"
        is Instruction.Sub -> "SUB \$${instr.address.toString(16).uppercase()}"
        is Instruction.Out -> "OUT"
        is Instruction.Hlt -> "HLT"
    }
}
