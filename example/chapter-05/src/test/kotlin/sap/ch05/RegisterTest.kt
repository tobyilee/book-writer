package sap.ch05

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class RegisterTest : DescribeSpec({
    describe("Register (8-bit)") {
        it("초기값 0") { Register().value shouldBe 0 }
        it("load 후 값 보유") {
            val r = Register(); r.load(42); r.value shouldBe 42
        }
        it("0xFF 넘는 값은 마스킹") {
            val r = Register(); r.load(0x123); r.value shouldBe 0x23
        }
        it("음수는 2의 보수 8비트로 마스킹") {
            val r = Register(); r.load(-1); r.value shouldBe 0xFF
        }
        it("clear로 0 복귀") {
            val r = Register(); r.load(99); r.clear(); r.value shouldBe 0
        }
    }
})
