package sap.ch08

class Clock {
    var tState: Int = 1
        private set

    fun tick() {
        tState = if (tState == 6) 1 else tState + 1
    }

    fun reset() {
        tState = 1
    }
}
