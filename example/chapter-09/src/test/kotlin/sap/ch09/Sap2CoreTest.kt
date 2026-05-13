package sap.ch09

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap2CoreTest : DescribeSpec({
    describe("Sap2Core") {
        it("64KB 메모리 + 16비트 PC 초기 상태") {
            val core = Sap2Core()
            core.memory.size shouldBe 65536
            core.pc shouldBe 0
            core.halted shouldBe false
        }
        it("setPc 16비트 마스킹") {
            val core = Sap2Core()
            core.setPc(0x12345)  // > 16 bits
            core.pc shouldBe 0x2345
        }
        it("PC가 0xFFFF에서 wrap") {
            val core = Sap2Core()
            core.setPc(0xFFFF)
            core.incrementPc()
            core.pc shouldBe 0
        }
        it("fetch는 메모리 읽고 PC 증가") {
            val core = Sap2Core()
            core.memory[0] = 0xAB
            core.memory[1] = 0xCD
            core.fetch() shouldBe 0xAB
            core.pc shouldBe 1
            core.fetch() shouldBe 0xCD
            core.pc shouldBe 2
        }
        it("writeByte/readByte 마스킹") {
            val core = Sap2Core()
            core.writeByte(0x1000, 0x12345)
            core.readByte(0x1000) shouldBe 0x45  // 8비트 마스킹
        }
        it("halt 후 halted=true") {
            val core = Sap2Core()
            core.halt()
            core.halted shouldBe true
        }
        it("reset은 메모리·PC·halted 모두 초기화") {
            val core = Sap2Core()
            core.writeByte(0x100, 0xFF)
            core.setPc(0x100)
            core.halt()
            core.reset()
            core.pc shouldBe 0
            core.halted shouldBe false
            core.memory[0x100] shouldBe 0
        }
    }
})
