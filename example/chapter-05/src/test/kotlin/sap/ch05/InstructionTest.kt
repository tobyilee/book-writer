package sap.ch05

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import io.kotest.matchers.types.shouldBeInstanceOf

class InstructionTest : DescribeSpec({
    describe("Instruction") {
        it("LDA 9 디코딩") {
            Instruction.decode(0x09) shouldBe Instruction.Lda(9)
        }
        it("ADD A 디코딩") {
            Instruction.decode(0x1A) shouldBe Instruction.Add(0xA)
        }
        it("SUB 5 디코딩") {
            Instruction.decode(0x25) shouldBe Instruction.Sub(5)
        }
        it("OUT 디코딩") {
            Instruction.decode(0xE0).shouldBeInstanceOf<Instruction.Out>()
        }
        it("HLT 디코딩") {
            Instruction.decode(0xF0).shouldBeInstanceOf<Instruction.Hlt>()
        }
        it("encode round-trip") {
            val original = Instruction.Lda(9)
            Instruction.decode(original.encode()) shouldBe original
        }
        it("알 수 없는 opcode는 예외") {
            try {
                Instruction.decode(0x70)
                error("expected exception")
            } catch (e: IllegalStateException) {
                // ok
            }
        }
    }
})
