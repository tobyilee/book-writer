package risc8.ch14

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class CycleAccurateTest : DescribeSpec({
    describe("CycleAccurateCpu") {
        it("ADD costs 1 cycle") {
            val cpu = CycleAccurateCpu(intArrayOf(Instruction.Add(1, 2, 3).encode()))
            cpu.step()
            cpu.cycleCount shouldBe 1L
        }

        it("LB costs 2 cycles") {
            val cpu = CycleAccurateCpu(intArrayOf(Instruction.Lb(rd = 1, rs1 = 0, imm = 0).encode()))
            cpu.step()
            cpu.cycleCount shouldBe 2L
        }

        it("SB costs 2 cycles") {
            val cpu = CycleAccurateCpu(intArrayOf(Instruction.Sb(rd = 1, rs1 = 0, imm = 0).encode()))
            cpu.step()
            cpu.cycleCount shouldBe 2L
        }

        it("JAL costs 2 cycles") {
            val cpu = CycleAccurateCpu(intArrayOf(Instruction.Jal(rd = 0, imm6 = 0).encode()))
            cpu.step()
            cpu.cycleCount shouldBe 2L
        }

        it("BEQ taken = 2 cycles") {
            // R0 == R0 항상 참, offset 0 — 자기 자신으로 점프 (분기 잡힘).
            val program = intArrayOf(
                Instruction.Beq(rd = 0, rs1 = 0, off = 0).encode(),
                Instruction.Halt().encode(),
            )
            val cpu = CycleAccurateCpu(program)
            cpu.step()
            cpu.cycleCount shouldBe 2L
        }

        it("BEQ not taken = 1 cycle") {
            // R1 = 5, BEQ R1, R0, +1 — 5 != 0 이라 분기 안 잡힘.
            val program = intArrayOf(
                Instruction.Li(rd = 1, imm6 = 5).encode(),
                Instruction.Beq(rd = 1, rs1 = 0, off = 1).encode(),
                Instruction.Halt().encode(),
            )
            val cpu = CycleAccurateCpu(program)
            cpu.step()   // LI — 1 cycle
            cpu.step()   // BEQ not taken — 1 cycle
            cpu.cycleCount shouldBe 2L
        }

        it("HALT은 1 cycle이고 그대로 halted 상태가 된다") {
            val cpu = CycleAccurateCpu(intArrayOf(Instruction.Halt().encode()))
            cpu.run()
            cpu.cycleCount shouldBe 1L
            cpu.halted shouldBe true
        }

        it("Fibonacci 프로그램: cycle 수 ≥ 명령어 수이고 메모리 결과는 동일하다") {
            val src = javaClass.classLoader.getResource("programs/fib.risc8")!!.readText()
            val program = Assembler.assemble(src)

            val ia = Cpu(program.words)
            ia.run()

            val ca = CycleAccurateCpu(program.words)
            ca.run()

            (ca.cycleCount >= ia.cyclesExecuted.toLong()) shouldBe true
            (0x10..0x19).map { ca.memory[it] } shouldBe listOf(0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
            (0x10..0x19).map { ia.memory[it] } shouldBe listOf(0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        }

        it("reset()은 cycleCount를 0으로 되돌린다") {
            val cpu = CycleAccurateCpu(intArrayOf(Instruction.Add(1, 2, 3).encode()))
            cpu.step()
            cpu.cycleCount shouldBe 1L
            cpu.reset()
            cpu.cycleCount shouldBe 0L
        }
    }
})
