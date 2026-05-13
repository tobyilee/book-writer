package sap.ch08

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import sap.ch08.asm.Assembler

class AssemblerTest : DescribeSpec({
    describe("Assembler 2-pass") {
        it("심볼 테이블에 라벨이 들어간다") {
            val asm = Assembler.assemble(
                """
                start: LDA ${'$'}9
                       HLT
                """.trimIndent(),
            )
            asm.symbols["start"] shouldBe 0
        }
        it("출력 바이트열이 정확하다") {
            val asm = Assembler.assemble("LDA \$9\nADD \$A\nOUT\nHLT")
            asm.bytes[0] shouldBe 0x09
            asm.bytes[1] shouldBe 0x1A
            asm.bytes[2] shouldBe 0xE0
            asm.bytes[3] shouldBe 0xF0
        }
        it("주소 디렉티브 9: \$2A") {
            val asm = Assembler.assemble("9: \$2A")
            asm.bytes[9] shouldBe 0x2A
        }
    }
})
