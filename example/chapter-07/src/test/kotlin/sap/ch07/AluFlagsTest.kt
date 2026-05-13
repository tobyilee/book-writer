package sap.ch07

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class AluFlagsTest : DescribeSpec({
    describe("AluFlags.add 기본 케이스") {
        it("0 + 0") {
            val r = AluFlags.add(0, 0)
            r.value shouldBe 0; r.zero shouldBe true; r.carry shouldBe false
            r.sign shouldBe false; r.overflow shouldBe false
        }
        it("100 + 50") {
            val r = AluFlags.add(100, 50)
            r.value shouldBe 150; r.zero shouldBe false; r.carry shouldBe false
            r.sign shouldBe true; r.overflow shouldBe true  // signed overflow: 100+50=150 > 127
        }
        it("255 + 1 (carry)") {
            val r = AluFlags.add(255, 1)
            r.value shouldBe 0; r.zero shouldBe true; r.carry shouldBe true
        }
        it("Sign 플래그 (음수 결과)") {
            val r = AluFlags.add(0x70, 0x70)  // signed 112 + 112 = 224, overflow
            r.value shouldBe 0xE0
            r.sign shouldBe true
            r.overflow shouldBe true
        }
    }
    describe("AluFlags.sub 기본") {
        it("10 - 5") {
            val r = AluFlags.sub(10, 5)
            r.value shouldBe 5; r.carry shouldBe true; r.zero shouldBe false
        }
        it("5 - 10 (borrow)") {
            val r = AluFlags.sub(5, 10)
            r.value shouldBe (0xFB)  // -5 as 2's comp
            r.carry shouldBe false  // borrow occurred
        }
    }
})
