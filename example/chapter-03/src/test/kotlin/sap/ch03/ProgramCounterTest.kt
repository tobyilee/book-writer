package sap.ch03

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class ProgramCounterTest : DescribeSpec({
    describe("ProgramCounter (4-bit)") {
        it("초기값 0") { ProgramCounter().value shouldBe 0 }
        it("increment 후 1 증가") {
            val pc = ProgramCounter(); pc.increment(); pc.value shouldBe 1
        }
        it("0xF에서 increment하면 wrap 0") {
            val pc = ProgramCounter()
            repeat(15) { pc.increment() }
            pc.value shouldBe 15
            pc.increment()
            pc.value shouldBe 0
        }
        it("reset으로 0 복귀") {
            val pc = ProgramCounter()
            pc.increment(); pc.increment()
            pc.reset()
            pc.value shouldBe 0
        }
        it("load는 4비트 마스킹") {
            val pc = ProgramCounter()
            pc.load(0x1F)
            pc.value shouldBe 0xF
        }
    }
})
