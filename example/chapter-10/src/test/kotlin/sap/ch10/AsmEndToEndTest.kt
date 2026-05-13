package sap.ch10

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import sap.ch10.asm.Assembler

class AsmEndToEndTest : DescribeSpec({
    describe("어셈블 → SAP-1 실행") {
        it("add.sap1을 어셈블하고 실행하면 OUT=47") {
            val src = javaClass.classLoader.getResource("programs/add.sap1")!!.readText()
            val program = Assembler.assemble(src)
            val sap1 = Sap1(program.bytes)
            sap1.run()
            sap1.output shouldBe 47
        }
        it("어셈블 → 디스어셈블 round-trip") {
            val src = """
                LDA ${'$'}9
                HLT
                9: ${'$'}2A
            """.trimIndent()
            val program = Assembler.assemble(src)
            program.bytes[0] shouldBe 0x09
            program.bytes[1] shouldBe 0xF0
            program.bytes[9] shouldBe 0x2A
        }
    }
})
