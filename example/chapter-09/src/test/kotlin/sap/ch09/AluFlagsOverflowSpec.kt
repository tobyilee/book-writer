package sap.ch09

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class AluFlagsOverflowSpec : DescribeSpec({
    describe("AluFlags.add — 모든 256×256 = 65,536 조합") {
        it("결과는 (a+b) mod 256") {
            for (a in 0..255) for (b in 0..255) {
                AluFlags.add(a, b).value shouldBe ((a + b) and 0xFF)
            }
        }
        it("Carry 플래그는 a+b >= 256일 때만 1") {
            for (a in 0..255) for (b in 0..255) {
                AluFlags.add(a, b).carry shouldBe ((a + b) >= 256)
            }
        }
        it("Zero 플래그는 결과가 0일 때만 1") {
            for (a in 0..255) for (b in 0..255) {
                AluFlags.add(a, b).zero shouldBe (((a + b) and 0xFF) == 0)
            }
        }
        it("Sign 플래그는 결과 비트7이 1일 때만 1") {
            for (a in 0..255) for (b in 0..255) {
                AluFlags.add(a, b).sign shouldBe (((a + b) and 0x80) != 0)
            }
        }
        it("Overflow 플래그는 부호 있는 overflow일 때만 1") {
            for (a in 0..255) for (b in 0..255) {
                val signedSum = a.toByte().toInt() + b.toByte().toInt()
                AluFlags.add(a, b).overflow shouldBe (signedSum < -128 || signedSum > 127)
            }
        }
    }
    describe("AluFlags.sub — 모든 256×256 = 65,536 조합") {
        it("결과는 (a-b) mod 256") {
            for (a in 0..255) for (b in 0..255) {
                AluFlags.sub(a, b).value shouldBe ((a - b) and 0xFF)
            }
        }
        it("Carry는 a >= b 일 때만 1 (no borrow)") {
            for (a in 0..255) for (b in 0..255) {
                AluFlags.sub(a, b).carry shouldBe (a >= b)
            }
        }
        it("Overflow signed 검증") {
            for (a in 0..255) for (b in 0..255) {
                val signedDiff = a.toByte().toInt() - b.toByte().toInt()
                AluFlags.sub(a, b).overflow shouldBe (signedDiff < -128 || signedDiff > 127)
            }
        }
    }
})
