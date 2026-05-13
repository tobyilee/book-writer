package risc8.ch14

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class AssemblerTest : DescribeSpec({
    describe("RISC-8 어셈블러") {
        it("ADD R1, R2, R3 한 줄") {
            val asm = Assembler.assemble("ADD R1, R2, R3")
            Instruction.decode(asm.words[0]) shouldBe Instruction.Add(1, 2, 3)
        }

        it("forward 참조 — BEQ가 뒤쪽 라벨을 가리킨다") {
            val src = """
                BEQ R0, R0, end
                LI  R1, 99
                end: HALT
            """.trimIndent()
            val asm = Assembler.assemble(src)
            asm.symbols["end"] shouldBe 2
            val beq = Instruction.decode(asm.words[0]) as Instruction.Beq
            beq.off shouldBe 1  // 타깃(2) - 현재(0) - 1 = 1
        }

        it("backward 참조 — JAL이 앞쪽 라벨을 가리킨다") {
            val src = """
                start: NOP
                       NOP
                       JAL R0, start
            """.trimIndent()
            val asm = Assembler.assemble(src)
            val jal = Instruction.decode(asm.words[2]) as Instruction.Jal
            jal.imm6 shouldBe -3  // 0 - 2 - 1 = -3
        }

        it("라벨·주석·여러 명령이 섞인 프로그램") {
            val src = """
                ; 도입 주석
                start: LI R1, 5     ; 5 로드
                       LI R2, 7
                       ADD R3, R1, R2
                       HALT
            """.trimIndent()
            val asm = Assembler.assemble(src)
            asm.symbols["start"] shouldBe 0
            asm.words.size shouldBe 4
            Instruction.decode(asm.words[2]) shouldBe Instruction.Add(3, 1, 2)
        }

        it("라벨만 있는 줄과 빈 줄을 처리한다") {
            val src = """

                label_only:
                       HALT
            """.trimIndent()
            val asm = Assembler.assemble(src)
            asm.symbols["label_only"] shouldBe 0
            asm.words.size shouldBe 1
            Instruction.decode(asm.words[0]) shouldBe Instruction.Halt()
        }

        it("16진수 즉치를 받는다") {
            val asm = Assembler.assemble("LI R1, 0x10")
            val li = Instruction.decode(asm.words[0]) as Instruction.Li
            li.imm6 shouldBe 16
        }

        it("음수 즉치를 받는다 (3-bit signed에 들어가도록)") {
            val asm = Assembler.assemble("ADDI R1, R1, -1")
            val addi = Instruction.decode(asm.words[0]) as Instruction.AddI
            addi.imm shouldBe -1
        }
    }
})
