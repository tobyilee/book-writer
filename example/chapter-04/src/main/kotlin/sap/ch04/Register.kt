package sap.ch04

class Register {
    var value: Int = 0
        private set
    fun load(v: Int) { value = v and 0xFF }
    fun clear() { value = 0 }
}
