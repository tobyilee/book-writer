package sap.ch10

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import io.kotest.matchers.string.shouldContain

class DebuggerTest : DescribeSpec({
    describe("Debugger") {
        // Simple program: LDI A,5; INC A; INC A; HLT
        //   bytes: 01 05 30 30 FF
        //   addresses: LDI@0..1, INC@2, INC@3, HLT@4
        fun setup(): Pair<Sap2, Debugger> {
            val cpu = Sap2()
            cpu.loadProgram(intArrayOf(0x01, 5, 0x30, 0x30, 0xFF))
            return cpu to Debugger(cpu)
        }

        it("step 한 번이 PC를 한 명령 진행") {
            val (cpu, dbg) = setup()
            val pcBefore = cpu.core.pc
            dbg.step()
            (cpu.core.pc > pcBefore) shouldBe true
        }
        it("registerDump이 PC/A/B/C/SP/Z/HALT 모두 포함") {
            val (_, dbg) = setup()
            val dump = dbg.registerDump()
            dump shouldContain "PC="
            dump shouldContain "A="
            dump shouldContain "B="
            dump shouldContain "C="
            dump shouldContain "SP="
            dump shouldContain "Z="
            dump shouldContain "HALT="
        }
        it("breakpoint에서 정지 — 그 명령은 아직 실행되지 않은 상태") {
            val (cpu, dbg) = setup()
            dbg.setBreakpoint(0x02) // 첫 INC A 위치
            dbg.continueUntilBreakOrHalt()
            cpu.core.pc shouldBe 0x02
            dbg.lastBreakpoint shouldBe 0x02
            cpu.regs.A.value shouldBe 5 // LDI만 실행되고 INC는 아직 안 함
        }
        it("breakpoint 없으면 HLT까지 진행") {
            val (cpu, dbg) = setup()
            dbg.continueUntilBreakOrHalt()
            cpu.core.halted shouldBe true
            cpu.regs.A.value shouldBe 7 // 5 + INC + INC
        }
        it("clearBreakpoint으로 제거 가능") {
            val (cpu, dbg) = setup()
            dbg.setBreakpoint(0x02)
            dbg.clearBreakpoint(0x02)
            dbg.listBreakpoints().size shouldBe 0
            dbg.continueUntilBreakOrHalt()
            cpu.core.halted shouldBe true
        }
        it("memoryDump 16바이트 형식 — 0x0000: 헤더 + 첫 바이트 01") {
            val (_, dbg) = setup()
            val dump = dbg.memoryDump(0, 16)
            dump shouldContain "0x0000:"
            dump shouldContain "01" // 첫 바이트: LDI A opcode
        }
    }
})
