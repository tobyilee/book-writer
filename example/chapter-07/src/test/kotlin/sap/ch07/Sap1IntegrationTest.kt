package sap.ch07

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap1IntegrationTest : DescribeSpec({
    describe("SAP-1 integration") {
        it("LDA 9 → ADD A → OUT → HLT 가 42+5=47 출력") {
            val rom = IntArray(16).apply {
                this[0] = 0x09
                this[1] = 0x1A
                this[2] = 0xE0
                this[3] = 0xF0
                this[9] = 0x2A
                this[10] = 0x05
            }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.output shouldBe 0x2F
            sap1.halted shouldBe true
        }
        it("HLT 단독 즉시 정지") {
            val rom = IntArray(16).apply { this[0] = 0xF0 }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.halted shouldBe true
        }
        it("SUB 명령") {
            val rom = IntArray(16).apply {
                this[0] = 0x09   // LDA 9 → A = 10
                this[1] = 0x2A   // SUB A (mem[10]) → A = 10 - 5 = 5
                this[2] = 0xE0
                this[3] = 0xF0
                this[9] = 0x0A
                this[10] = 0x05
            }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.output shouldBe 0x05
        }
        it("연속 OUT은 마지막 값") {
            // LDA 9 → OUT (42) → LDA A → OUT (5) → HLT
            val rom = IntArray(16).apply {
                this[0] = 0x09
                this[1] = 0xE0
                this[2] = 0x0A
                this[3] = 0xE0
                this[4] = 0xF0
                this[9] = 0x2A
                this[10] = 0x05
            }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.output shouldBe 0x05
        }
        it("ADD overflow는 8비트 wrap") {
            val rom = IntArray(16).apply {
                this[0] = 0x09  // LDA 9 → A = 200
                this[1] = 0x1A  // ADD A (mem[10]=100) → A = 44
                this[2] = 0xE0
                this[3] = 0xF0
                this[9] = 0xC8
                this[10] = 0x64
            }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.output shouldBe 0x2C
        }
        it("cycle count는 명령어 수와 일치") {
            val rom = IntArray(16).apply {
                this[0] = 0x09; this[1] = 0x1A; this[2] = 0xE0; this[3] = 0xF0
                this[9] = 0x2A; this[10] = 0x05
            }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.cyclesExecuted shouldBe 4  // LDA, ADD, OUT, HLT
        }
    }
    describe("Ram") {
        it("16바이트 메모리 read/write") {
            val ram = Ram()
            ram.write(5, 0x42)
            ram.read(5) shouldBe 0x42
        }
        it("주소는 4비트 마스킹") {
            val ram = Ram()
            ram.write(0x1F, 0xAA)
            ram.read(0xF) shouldBe 0xAA
        }
    }
    describe("Controller") {
        it("LDA T4에서 MEM_READ + LOAD_A 신호") {
            val sig = Controller.signalsFor(opcode = 0x09, tState = 4)
            (ControlSignal.MEM_READ in sig) shouldBe true
            (ControlSignal.LOAD_A in sig) shouldBe true
        }
        it("HLT T4에서 HALT 신호") {
            val sig = Controller.signalsFor(opcode = 0xF0, tState = 4)
            (ControlSignal.HALT in sig) shouldBe true
        }
    }
})
