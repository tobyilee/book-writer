package sap.ch09

class Sap2Core {
    val memory: IntArray = IntArray(65536)
    var pc: Int = 0
        private set
    var halted: Boolean = false
        private set

    fun setPc(v: Int) { pc = v and 0xFFFF }
    fun incrementPc() { pc = (pc + 1) and 0xFFFF }
    fun fetch(): Int {
        val byte = memory[pc] and 0xFF
        incrementPc()
        return byte
    }
    fun writeByte(addr: Int, value: Int) {
        memory[addr and 0xFFFF] = value and 0xFF
    }
    fun readByte(addr: Int): Int = memory[addr and 0xFFFF] and 0xFF
    fun halt() { halted = true }
    fun reset() {
        pc = 0
        halted = false
        memory.fill(0)
    }
}
