package sap.ch02

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class MiniCpuTest : DescribeSpec({
    describe("MiniCpu") {
        it("HLT 단일 명령으로 즉시 정지") {
            val cpu = MiniCpu(memory = intArrayOf(0x10))
            cpu.run()
            cpu.halted shouldBe true
            cpu.accumulator shouldBe 0
        }
        it("ADD <addr> 후 HLT 시 누산기에 합산") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 3, 0x10, 42))
            cpu.run()
            cpu.accumulator shouldBe 42
        }
        it("두 번의 ADD 누적") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 5, 0x01, 6, 0x10, 10, 20))
            cpu.run()
            cpu.accumulator shouldBe 30
        }
        it("PC가 메모리 끝을 넘으면 즉시 정지") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 1))
            cpu.run()
            cpu.halted shouldBe true
        }
        it("HLT 만나기 전까지 fetch-decode-execute 반복") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 5, 0x01, 6, 0x10, 7, 8))
            cpu.run()
            cpu.accumulator shouldBe 15
        }
        it("초기 상태에서 PC=0, accumulator=0") {
            val cpu = MiniCpu(memory = intArrayOf(0x10))
            cpu.pc shouldBe 0
            cpu.accumulator shouldBe 0
        }
        it("실행 후 PC가 HLT 다음 위치로 이동") {
            val cpu = MiniCpu(memory = intArrayOf(0x10, 99))
            cpu.run()
            cpu.pc shouldBe 1
        }
        it("ADD 후 PC는 2칸 전진, HLT 후 1칸 더") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 3, 0x10, 5))
            cpu.run()
            cpu.pc shouldBe 3
        }
    }
})
