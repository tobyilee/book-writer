package sap.ch09

import sap.ch09.asm.Sap2Assembler

fun main() {
    val src = Sap2::class.java.classLoader.getResource("programs/hello.sap2")!!.readText()
    val bytes = Sap2Assembler.assemble(src)
    val sap2 = Sap2()
    sap2.loadProgram(bytes)
    sap2.run()
    print(sap2.port0Output)
}
