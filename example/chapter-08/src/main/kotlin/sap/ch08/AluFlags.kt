package sap.ch08

data class AluResult(
    val value: Int,
    val zero: Boolean,
    val carry: Boolean,
    val sign: Boolean,
    val overflow: Boolean,
)

object AluFlags {
    fun add(a: Int, b: Int): AluResult {
        val full = a + b
        val v = full and 0xFF
        val signedA = a.toByte().toInt()
        val signedB = b.toByte().toInt()
        val signedSum = signedA + signedB
        return AluResult(
            value = v,
            zero = v == 0,
            carry = full >= 256,
            sign = (v and 0x80) != 0,
            overflow = signedSum < -128 || signedSum > 127,
        )
    }

    fun sub(a: Int, b: Int): AluResult {
        val full = a - b
        val v = full and 0xFF
        val signedA = a.toByte().toInt()
        val signedB = b.toByte().toInt()
        val signedDiff = signedA - signedB
        return AluResult(
            value = v,
            zero = v == 0,
            carry = a >= b,  // SBC: carry=1 means no borrow
            sign = (v and 0x80) != 0,
            overflow = signedDiff < -128 || signedDiff > 127,
        )
    }

    fun and(a: Int, b: Int): AluResult {
        val v = (a and b) and 0xFF
        return AluResult(v, zero = v == 0, carry = false, sign = (v and 0x80) != 0, overflow = false)
    }

    fun or(a: Int, b: Int): AluResult {
        val v = (a or b) and 0xFF
        return AluResult(v, zero = v == 0, carry = false, sign = (v and 0x80) != 0, overflow = false)
    }

    fun xor(a: Int, b: Int): AluResult {
        val v = (a xor b) and 0xFF
        return AluResult(v, zero = v == 0, carry = false, sign = (v and 0x80) != 0, overflow = false)
    }
}
