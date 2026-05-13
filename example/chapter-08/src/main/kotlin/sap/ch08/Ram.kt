package sap.ch08

class Ram(initial: IntArray = IntArray(16)) {
    private val mem = IntArray(16)

    init {
        initial.copyInto(mem, endIndex = minOf(initial.size, 16))
    }

    fun read(addr: Int): Int = mem[addr and 0xF]

    fun write(addr: Int, value: Int) {
        mem[addr and 0xF] = value and 0xFF
    }

    fun snapshot(): IntArray = mem.copyOf()
}
