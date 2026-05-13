package sap.ch06

fun main() {
    val rom = IntArray(16).apply {
        this[0] = 0x09  // LDA 9
        this[1] = 0x1A  // ADD A (mem[10])
        this[2] = 0xE0  // OUT
        this[3] = 0xF0  // HLT
        this[9] = 0x2A  // 42
        this[10] = 0x05 // 5
    }
    val sap1 = Sap1(rom)
    sap1.run()
    println("OUT = ${sap1.output} (0x${sap1.output.toString(16).uppercase()})")
    println("Cycles: ${sap1.cyclesExecuted}")
}
