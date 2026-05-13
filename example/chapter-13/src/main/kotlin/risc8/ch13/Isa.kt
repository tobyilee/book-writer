package risc8.ch13

/**
 * RISC-8 ISA — 16비트 고정 길이 명령어.
 *
 * 비트 배치 (15..0):
 * ```
 * R-type: [opcode:7][rd:3][rs1:3][rs2:3]
 * I-type: [opcode:7][rd:3][rs1:3][imm:3]    (imm은 sign-extended 3-bit; LB/SB·JR는 zero-ext처럼 쓴다)
 * J-type: [opcode:7][rd:3][imm6:6]          (분기 오프셋용 6-bit sign-extended)
 * L-type: [opcode:7][rd:3][imm6:6]          (LI 전용 6-bit zero-extended)
 * ```
 *
 * 3-bit 레지스터 필드만 쓰므로 실효 레지스터는 R0..R7 — 본 책의 RISC-8 명세.
 */
sealed class Instruction(val opcode: Int) {
    abstract fun encode(): Int

    data class Nop(val placeholder: Int = 0) : Instruction(0x00) {
        override fun encode(): Int = 0
    }
    data class Add(val rd: Int, val rs1: Int, val rs2: Int) : Instruction(0x01) {
        override fun encode(): Int = encR(0x01, rd, rs1, rs2)
    }
    data class Sub(val rd: Int, val rs1: Int, val rs2: Int) : Instruction(0x02) {
        override fun encode(): Int = encR(0x02, rd, rs1, rs2)
    }
    data class And(val rd: Int, val rs1: Int, val rs2: Int) : Instruction(0x03) {
        override fun encode(): Int = encR(0x03, rd, rs1, rs2)
    }
    data class Or(val rd: Int, val rs1: Int, val rs2: Int) : Instruction(0x04) {
        override fun encode(): Int = encR(0x04, rd, rs1, rs2)
    }
    data class Xor(val rd: Int, val rs1: Int, val rs2: Int) : Instruction(0x05) {
        override fun encode(): Int = encR(0x05, rd, rs1, rs2)
    }
    data class Shl(val rd: Int, val rs1: Int, val rs2: Int) : Instruction(0x06) {
        override fun encode(): Int = encR(0x06, rd, rs1, rs2)
    }
    data class Shr(val rd: Int, val rs1: Int, val rs2: Int) : Instruction(0x07) {
        override fun encode(): Int = encR(0x07, rd, rs1, rs2)
    }
    data class AddI(val rd: Int, val rs1: Int, val imm: Int) : Instruction(0x10) {
        override fun encode(): Int = encI(0x10, rd, rs1, imm)
    }
    data class AndI(val rd: Int, val rs1: Int, val imm: Int) : Instruction(0x11) {
        override fun encode(): Int = encI(0x11, rd, rs1, imm)
    }
    data class Lb(val rd: Int, val rs1: Int, val imm: Int) : Instruction(0x20) {
        override fun encode(): Int = encI(0x20, rd, rs1, imm)
    }
    data class Sb(val rd: Int, val rs1: Int, val imm: Int) : Instruction(0x21) {
        override fun encode(): Int = encI(0x21, rd, rs1, imm)
    }
    data class Beq(val rd: Int, val rs1: Int, val off: Int) : Instruction(0x30) {
        override fun encode(): Int = encI(0x30, rd, rs1, off)
    }
    data class Bne(val rd: Int, val rs1: Int, val off: Int) : Instruction(0x31) {
        override fun encode(): Int = encI(0x31, rd, rs1, off)
    }
    data class Jal(val rd: Int, val imm6: Int) : Instruction(0x40) {
        override fun encode(): Int = encJ(0x40, rd, imm6)
    }
    data class Jr(val rd: Int, val rs1: Int, val imm: Int) : Instruction(0x41) {
        override fun encode(): Int = encI(0x41, rd, rs1, imm)
    }
    data class Li(val rd: Int, val imm6: Int) : Instruction(0x50) {
        override fun encode(): Int = encJ(0x50, rd, imm6)
    }
    data class Ecall(val placeholder: Int = 0) : Instruction(0x60) {
        override fun encode(): Int = 0x60 shl 9
    }
    data class Ebreak(val placeholder: Int = 0) : Instruction(0x61) {
        override fun encode(): Int = 0x61 shl 9
    }
    data class Halt(val placeholder: Int = 0) : Instruction(0x7F) {
        override fun encode(): Int = 0x7F shl 9
    }

    companion object {
        fun decode(word: Int): Instruction {
            val w = word and 0xFFFF
            val op = (w shr 9) and 0x7F
            val rd = (w shr 6) and 0x7
            val rs1 = (w shr 3) and 0x7
            val rs2 = w and 0x7
            val imm3Signed = signExt3(rs2)
            val imm6 = w and 0x3F  // J/L-type용 raw 6-bit
            return when (op) {
                0x00 -> Nop()
                0x01 -> Add(rd, rs1, rs2)
                0x02 -> Sub(rd, rs1, rs2)
                0x03 -> And(rd, rs1, rs2)
                0x04 -> Or(rd, rs1, rs2)
                0x05 -> Xor(rd, rs1, rs2)
                0x06 -> Shl(rd, rs1, rs2)
                0x07 -> Shr(rd, rs1, rs2)
                0x10 -> AddI(rd, rs1, imm3Signed)
                0x11 -> AndI(rd, rs1, imm3Signed)
                0x20 -> Lb(rd, rs1, rs2)          // 메모리 오프셋은 unsigned 3-bit
                0x21 -> Sb(rd, rs1, rs2)
                0x30 -> Beq(rd, rs1, imm3Signed)
                0x31 -> Bne(rd, rs1, imm3Signed)
                0x40 -> Jal(rd, signExt6(imm6))
                0x41 -> Jr(rd, rs1, imm3Signed)
                0x50 -> Li(rd, imm6)              // LI는 6-bit zero-extended
                0x60 -> Ecall()
                0x61 -> Ebreak()
                0x7F -> Halt()
                else -> error("Unknown opcode: 0x${op.toString(16)}")
            }
        }

        private fun encR(op: Int, rd: Int, rs1: Int, rs2: Int): Int =
            ((op and 0x7F) shl 9) or
                ((rd and 0x7) shl 6) or
                ((rs1 and 0x7) shl 3) or
                (rs2 and 0x7)

        private fun encI(op: Int, rd: Int, rs1: Int, imm: Int): Int =
            ((op and 0x7F) shl 9) or
                ((rd and 0x7) shl 6) or
                ((rs1 and 0x7) shl 3) or
                (imm and 0x7)

        private fun encJ(op: Int, rd: Int, imm6: Int): Int =
            ((op and 0x7F) shl 9) or
                ((rd and 0x7) shl 6) or
                (imm6 and 0x3F)

        private fun signExt3(v: Int): Int = if (v and 0x4 != 0) v or 0xFFFFFFF8.toInt() else v
        private fun signExt6(v: Int): Int = if (v and 0x20 != 0) v or 0xFFFFFFC0.toInt() else v
    }
}
