package sap.ch10

import sap.ch10.asm.Sap2Assembler

/**
 * SAP-2 디버거의 REPL CLI.
 *
 * 명령:
 *   s         — step (한 명령 실행)
 *   c         — continue (breakpoint 또는 HLT까지)
 *   b <addr>  — breakpoint 설정 (10진/0x16진/$16진)
 *   r         — 레지스터 덤프
 *   m <addr>  — 메모리 16바이트 덤프
 *   q         — 종료
 *
 * 기본 프로그램은 resources/programs/hello.sap2.
 */
fun main() {
    val cpu = Sap2()
    val helloSrc = object {}.javaClass.classLoader.getResource("programs/hello.sap2")?.readText()
    if (helloSrc != null) {
        cpu.loadProgram(Sap2Assembler.assemble(helloSrc))
    }
    val dbg = Debugger(cpu)

    println("SAP-2 디버거 — 명령: s(tep) c(ontinue) b <addr> r(egisters) m <addr> q(uit)")
    println(dbg.registerDump())

    while (true) {
        print("> ")
        val line = readLine()?.trim() ?: break
        if (line.isEmpty()) continue
        val parts = line.split(Regex("\\s+"))
        when (parts[0]) {
            "s" -> { dbg.step(); println(dbg.registerDump()) }
            "c" -> {
                dbg.continueUntilBreakOrHalt()
                val brk = dbg.lastBreakpoint
                if (brk != null) println("Breakpoint at 0x${brk.toString(16).uppercase()}")
                else if (dbg.halted) println("CPU halted")
                println(dbg.registerDump())
            }
            "b" -> {
                if (parts.size > 1) {
                    val addr = parseAddr(parts[1])
                    dbg.setBreakpoint(addr)
                    println("Breakpoint set at 0x${addr.toString(16).uppercase()}")
                } else println("Usage: b <addr>")
            }
            "r" -> println(dbg.registerDump())
            "m" -> {
                val addr = if (parts.size > 1) parseAddr(parts[1]) else 0
                print(dbg.memoryDump(addr, 16))
            }
            "q" -> { println("Goodbye"); return }
            else -> println("Unknown: ${parts[0]}")
        }
    }
}

private fun parseAddr(s: String): Int = when {
    s.startsWith("0x") -> s.substring(2).toInt(16)
    s.startsWith("$") -> s.drop(1).toInt(16)
    else -> s.toInt()
}
