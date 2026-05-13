package sap.ch10

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap2InstructionsTest : DescribeSpec({
    describe("SAP-2 명령어들") {
        it("LDI A, 42 → A=42") {
            val sap2 = assembleAndRun("LDI A, 42\nHLT")
            sap2.regs.A.value shouldBe 42
        }
        it("MOV B, A 후 B==A") {
            val sap2 = assembleAndRun("LDI A, 99\nMOV B, A\nHLT")
            sap2.regs.B.value shouldBe 99
        }
        it("ADD B 가 A = A + B 를 한다") {
            val sap2 = assembleAndRun("LDI A, 10\nLDI B, 5\nADD B\nHLT")
            sap2.regs.A.value shouldBe 15
        }
        it("SUB B 가 A = A - B 를 한다") {
            val sap2 = assembleAndRun("LDI A, 10\nLDI B, 4\nSUB B\nHLT")
            sap2.regs.A.value shouldBe 6
        }
        it("DEC A 후 A 가 1 감소한다") {
            val sap2 = assembleAndRun("LDI A, 5\nDEC A\nHLT")
            sap2.regs.A.value shouldBe 4
        }
        it("DEC A 가 0이면 zero flag 가 세팅되고 JZ 가 점프한다") {
            val sap2 = assembleAndRun(
                """
                        LDI A, 1
                        DEC A
                        JZ  end
                        LDI A, 99
                end:    HLT
                """.trimIndent(),
            )
            sap2.regs.A.value shouldBe 0
            sap2.zeroFlag shouldBe true
        }
        it("zero flag 가 false 면 JNZ 가 점프한다") {
            val sap2 = assembleAndRun(
                """
                        LDI A, 2
                        DEC A             ; A=1, Z=false
                        JNZ skip
                        LDI A, 99
                skip:   HLT
                """.trimIndent(),
            )
            sap2.regs.A.value shouldBe 1
            sap2.zeroFlag shouldBe false
        }
        it("JMP 는 무조건 점프한다") {
            val sap2 = assembleAndRun(
                """
                        JMP target
                        LDI A, 99
                target: LDI A, 7
                        HLT
                """.trimIndent(),
            )
            sap2.regs.A.value shouldBe 7
        }
        it("CALL/RET 가 서브루틴을 호출하고 복귀한다") {
            val sap2 = assembleAndRun(
                """
                        LDI A, 5
                        CALL inc_a
                        HLT
                inc_a:  INC A
                        RET
                """.trimIndent(),
            )
            sap2.regs.A.value shouldBe 6
        }
        it("CALL 후 SP 가 2 감소하고 RET 후 원복된다") {
            // CALL 직전 SP=0xFFFE, CALL 후 0xFFFC, RET 후 0xFFFE
            val sap2 = assembleAndRun(
                """
                        CALL sub
                        HLT
                sub:    RET
                """.trimIndent(),
            )
            sap2.sp shouldBe 0xFFFE
        }
        it("OUT 0 은 port0 history 와 ASCII 버퍼에 기록된다") {
            val sap2 = assembleAndRun("LDI A, 65\nOUT 0\nHLT")
            sap2.port0OutputBytes shouldBe listOf(65)
            sap2.port0Output shouldBe "A"
        }
        it("IN 포트로 외부에서 주입한 값을 A 에 적재한다") {
            val sap2 = sap.ch10.Sap2()
            sap2.setInputPort(3, 0x7F)
            val bytes = sap.ch10.asm.Sap2Assembler.assemble("IN 3\nHLT")
            sap2.loadProgram(bytes)
            sap2.run()
            sap2.regs.A.value shouldBe 0x7F
        }
        it("INC 가 0xFF 를 넘어가면 0으로 wrap 되고 zero flag 가 세팅된다") {
            val sap2 = assembleAndRun("LDI A, 0xFF\nINC A\nHLT")
            sap2.regs.A.value shouldBe 0
            sap2.zeroFlag shouldBe true
        }
        it("문자 리터럴은 ASCII 코드로 어셈블된다") {
            val sap2 = assembleAndRun("LDI A, 'Z'\nHLT")
            sap2.regs.A.value shouldBe 'Z'.code
        }
    }
})
