package risc8.ch14

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class IsaTest : DescribeSpec({
    describe("RISC-8 ISA — encode/decode 라운드트립") {
        it("ADD R1, R2, R3") {
            val instr = Instruction.Add(rd = 1, rs1 = 2, rs2 = 3)
            Instruction.decode(instr.encode()) shouldBe instr
        }
        it("SUB R7, R6, R5") {
            val instr = Instruction.Sub(rd = 7, rs1 = 6, rs2 = 5)
            Instruction.decode(instr.encode()) shouldBe instr
        }
        it("LI R3, 16 (6-bit zero-extended 즉치)") {
            val instr = Instruction.Li(rd = 3, imm6 = 16)
            Instruction.decode(instr.encode()) shouldBe instr
        }
        it("ADDI R1, R2, -1 (3-bit signed)") {
            val instr = Instruction.AddI(rd = 1, rs1 = 2, imm = -1)
            Instruction.decode(instr.encode()) shouldBe instr
        }
        it("BEQ R1, R2, -3 (negative 3-bit signed offset)") {
            val instr = Instruction.Beq(rd = 1, rs1 = 2, off = -3)
            Instruction.decode(instr.encode()) shouldBe instr
        }
        it("JAL R0, -9 (negative 6-bit signed offset)") {
            val instr = Instruction.Jal(rd = 0, imm6 = -9)
            Instruction.decode(instr.encode()) shouldBe instr
        }
        it("HALT") {
            val w = Instruction.Halt().encode()
            Instruction.decode(w) shouldBe Instruction.Halt()
        }
        it("NOP은 모두 0인 워드") {
            Instruction.Nop().encode() shouldBe 0
            Instruction.decode(0) shouldBe Instruction.Nop()
        }
        it("LB rd, rs1, imm — 메모리 명령어 라운드트립") {
            val instr = Instruction.Lb(rd = 4, rs1 = 5, imm = 6)
            Instruction.decode(instr.encode()) shouldBe instr
        }
    }

    describe("비트 레이아웃 검증") {
        it("ADD R1, R2, R3 은 16-bit 안에 들어간다") {
            val w = Instruction.Add(1, 2, 3).encode()
            (w and 0xFFFF) shouldBe w  // 음수/오버플로 없음
            (w shr 9) shouldBe 0x01    // opcode 자리
            ((w shr 6) and 0x7) shouldBe 1
            ((w shr 3) and 0x7) shouldBe 2
            (w and 0x7) shouldBe 3
        }
        it("HALT의 opcode는 0x7F") {
            val w = Instruction.Halt().encode()
            ((w shr 9) and 0x7F) shouldBe 0x7F
        }
    }
})
