package sap.ch10

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

/**
 * Test ROM 회귀 검증 — 책에서 말한 "6502 functional test의 SAP-2 축소판".
 *
 * 각 ROM은 ISA의 한 영역(산술/분기/CALL-RET)을 좁게 짚어 결정적인 종료 상태를 만든다.
 * CPU 구조를 바꿔도 이 ROM들이 통과하면 외부 동작은 그대로다 — 그게 회귀 테스트의 약속이다.
 */
class Sap2TestRomSpec : DescribeSpec({
    describe("SAP-2 test ROM (회귀 검증)") {
        it("산술 ROM: 5 + 3 - 1 = 7") {
            val cpu = Sap2()
            // LDI A,5; LDI B,3; ADD B; DEC A; HLT
            cpu.loadProgram(intArrayOf(0x01, 5, 0x02, 3, 0x20, 0x33, 0xFF))
            cpu.run()
            cpu.regs.A.value shouldBe 7
            cpu.zeroFlag shouldBe false
        }
        it("분기 ROM: counter loop, A=0 종료") {
            val cpu = Sap2()
            // LDI A, 3; loop: DEC A; JNZ loop; HLT
            //   bytes: 01 03  33  42 02 00  FF
            //   addresses: LDI@0..1, DEC@2, JNZ@3..5, HLT@6
            //   JNZ target = 0x0002 (DEC 위치)
            cpu.loadProgram(intArrayOf(0x01, 3, 0x33, 0x42, 0x02, 0x00, 0xFF))
            cpu.run()
            cpu.regs.A.value shouldBe 0
            cpu.zeroFlag shouldBe true
        }
        it("CALL/RET ROM: subroutine이 A에 10을 더한다") {
            val cpu = Sap2()
            // main:   LDI A, 5      @0..1
            //         CALL add_10   @2..4   (CALL은 3바이트: 0x50 lo hi)
            //         HLT           @5
            // add_10: LDI B, 10     @6..7
            //         ADD B         @8
            //         RET           @9
            cpu.loadProgram(intArrayOf(
                0x01, 5,
                0x50, 6, 0,
                0xFF,
                0x02, 10,
                0x20,
                0x51,
            ))
            cpu.run()
            cpu.regs.A.value shouldBe 15
        }
    }
})
