package sap.ch04

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import io.kotest.data.forAll
import io.kotest.data.row

class AluTest : DescribeSpec({
    describe("Alu 산술") {
        it("ADD 기본") {
            Alu.add(10, 20) shouldBe 30
            Alu.add(0, 0) shouldBe 0
        }
        it("ADD 8비트 wrap") {
            Alu.add(255, 1) shouldBe 0
            Alu.add(100, 200) shouldBe 44  // 300 mod 256
        }
        it("SUB") {
            Alu.sub(50, 10) shouldBe 40
        }
        it("SUB borrow (음수 결과는 2의 보수로)") {
            Alu.sub(0, 1) shouldBe 0xFF
            Alu.sub(10, 50) shouldBe ((10 - 50) and 0xFF)
        }
        it("산술 표 기반 검증") {
            forAll(
                row(0, 0, 0),
                row(1, 1, 2),
                row(127, 1, 128),
                row(255, 255, 254),
                row(100, 200, 44),
            ) { a, b, expected -> Alu.add(a, b) shouldBe expected }
        }
    }
    describe("Alu 논리") {
        it("AND") { Alu.and(0b11110000, 0b10101010) shouldBe 0b10100000 }
        it("OR") { Alu.or(0b11110000, 0b00001111) shouldBe 0xFF }
        it("XOR") { Alu.xor(0xFF, 0x0F) shouldBe 0xF0 }
        it("NOT") {
            Alu.not(0x00) shouldBe 0xFF
            Alu.not(0xFF) shouldBe 0x00
            Alu.not(0xAA) shouldBe 0x55
        }
    }
})
