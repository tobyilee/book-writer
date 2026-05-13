package sap.ch10

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.collections.shouldContain
import io.kotest.matchers.collections.shouldNotContain

class MicroRomTest : DescribeSpec({
    describe("MicroRom — SAP-1 control matrix") {
        it("Fetch T1: PC_OUT + MAR_LOAD (모든 명령 공통)") {
            val sig = MicroRom.signalsFor(opcode = 0x09, tState = 1)
            sig shouldContain MicroSignal.PC_OUT
            sig shouldContain MicroSignal.MAR_LOAD
        }
        it("Fetch T2: PC_INC만 활성") {
            val sig = MicroRom.signalsFor(opcode = 0x1A, tState = 2)
            sig shouldContain MicroSignal.PC_INC
        }
        it("Fetch T3: MEM_OUT + IR_LOAD") {
            val sig = MicroRom.signalsFor(opcode = 0x09, tState = 3)
            sig shouldContain MicroSignal.MEM_OUT
            sig shouldContain MicroSignal.IR_LOAD
        }
        it("LDA T4: IR_OUT + MAR_LOAD") {
            val sig = MicroRom.signalsFor(opcode = 0x09, tState = 4) // LDA
            sig shouldContain MicroSignal.IR_OUT
            sig shouldContain MicroSignal.MAR_LOAD
        }
        it("LDA T5: MEM_OUT + A_LOAD") {
            val sig = MicroRom.signalsFor(opcode = 0x09, tState = 5)
            sig shouldContain MicroSignal.MEM_OUT
            sig shouldContain MicroSignal.A_LOAD
        }
        it("ADD T6: ALU_OUT + A_LOAD, SUB_MODE는 꺼져 있다") {
            val sig = MicroRom.signalsFor(opcode = 0x1A, tState = 6) // ADD
            sig shouldContain MicroSignal.ALU_OUT
            sig shouldContain MicroSignal.A_LOAD
            sig shouldNotContain MicroSignal.ALU_SUB_MODE
        }
        it("SUB T6: ALU_SUB_MODE 포함") {
            val sig = MicroRom.signalsFor(opcode = 0x2A, tState = 6) // SUB
            sig shouldContain MicroSignal.ALU_SUB_MODE
            sig shouldContain MicroSignal.A_LOAD
        }
        it("OUT T4: A_OUT + OUT_LOAD") {
            val sig = MicroRom.signalsFor(opcode = 0xE0, tState = 4)
            sig shouldContain MicroSignal.A_OUT
            sig shouldContain MicroSignal.OUT_LOAD
        }
        it("HLT T4: HALT signal") {
            val sig = MicroRom.signalsFor(opcode = 0xF0, tState = 4)
            sig shouldContain MicroSignal.HALT
        }
    }
})
