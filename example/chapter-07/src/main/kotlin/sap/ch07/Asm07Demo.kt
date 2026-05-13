package sap.ch07

import sap.ch07.asm.Assembler
import sap.ch07.asm.Disassembler

fun main() {
    val src = object {}.javaClass.classLoader.getResource("programs/add.sap1")!!.readText()
    println("--- Source ---")
    println(src)

    val program = Assembler.assemble(src)

    println("--- Symbols ---")
    program.symbols.forEach { (n, a) -> println("  $n -> 0x${a.toString(16).uppercase()}") }

    println("--- Bytes (16 hex) ---")
    println(program.bytes.joinToString(" ") { "0x${it.toString(16).padStart(2, '0').uppercase()}" })

    println("--- Disassembly ---")
    print(Disassembler.bytesToText(program.bytes))

    val sap1 = Sap1(program.bytes)
    sap1.run()
    println("--- Execution ---")
    println("OUT = ${sap1.output} (0x${sap1.output.toString(16).uppercase()})")
    println("Cycles: ${sap1.cyclesExecuted}")
}
