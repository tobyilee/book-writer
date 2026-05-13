package risc8.ch13

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class CpuFibTest : DescribeSpec({
    describe("RISC-8 CPU — 기본 동작") {
        it("LI + ADD — 5 + 7 = 12") {
            val asm = Assembler.assemble(
                """
                LI R1, 5
                LI R2, 7
                ADD R3, R1, R2
                HALT
                """.trimIndent()
            )
            val cpu = Cpu(asm.words)
            cpu.run()
            cpu.registers[1] shouldBe 5
            cpu.registers[2] shouldBe 7
            cpu.registers[3] shouldBe 12
            cpu.halted shouldBe true
        }

        it("R0은 쓰기를 무시한다 (항상 0)") {
            val asm = Assembler.assemble(
                """
                LI R0, 42
                HALT
                """.trimIndent()
            )
            val cpu = Cpu(asm.words)
            cpu.run()
            cpu.registers[0] shouldBe 0
        }

        it("BEQ + JAL 로 카운트다운 루프가 종료한다") {
            val asm = Assembler.assemble(
                """
                       LI R1, 3
                       LI R2, 0
                loop:  ADDI R1, R1, -1
                       BEQ R1, R2, end
                       JAL R0, loop
                end:   HALT
                """.trimIndent()
            )
            val cpu = Cpu(asm.words)
            cpu.run()
            cpu.registers[1] shouldBe 0
            cpu.halted shouldBe true
        }

        it("SB + LB — 메모리 라운드트립") {
            val asm = Assembler.assemble(
                """
                LI R1, 42
                LI R2, 0x20
                SB R1, R2, 0
                LB R3, R2, 0
                HALT
                """.trimIndent()
            )
            val cpu = Cpu(asm.words)
            cpu.run()
            cpu.memory[0x20] shouldBe 42
            cpu.registers[3] shouldBe 42
        }

        it("8-bit 연산은 0xFF로 wrap된다") {
            val asm = Assembler.assemble(
                """
                LI R1, 0x3F
                LI R2, 0x3F
                ADD R3, R1, R2     ; 0x7E
                ADD R3, R3, R3     ; 0xFC
                ADD R3, R3, R3     ; 0x1F8 -> 0xF8
                HALT
                """.trimIndent()
            )
            val cpu = Cpu(asm.words)
            cpu.run()
            cpu.registers[3] shouldBe 0xF8
        }
    }

    describe("RISC-8 CPU — Fibonacci 통합") {
        it("fib.risc8 가 F(0)..F(9) = 0,1,1,2,3,5,8,13,21,34 를 메모리에 남긴다") {
            val src = javaClass.classLoader.getResource("programs/fib.risc8")
                ?.readText()
                ?: error("programs/fib.risc8 를 찾지 못했다")
            val asm = Assembler.assemble(src)
            val cpu = Cpu(asm.words)
            cpu.run()
            cpu.halted shouldBe true
            val fibs = (0x10..0x19).map { cpu.memory[it] }
            fibs shouldBe listOf(0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        }
    }
})
