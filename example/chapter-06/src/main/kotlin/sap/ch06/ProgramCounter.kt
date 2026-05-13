package sap.ch06

class ProgramCounter {
    var value: Int = 0
        private set

    fun increment() {
        value = (value + 1) and 0xF
    }

    fun reset() {
        value = 0
    }

    fun load(v: Int) {
        value = v and 0xF
    }
}
