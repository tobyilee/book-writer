package sap.ch08

class RegisterFile {
    val A: Register = Register()
    val B: Register = Register()
    val C: Register = Register()

    fun reset() {
        A.clear(); B.clear(); C.clear()
    }
}
