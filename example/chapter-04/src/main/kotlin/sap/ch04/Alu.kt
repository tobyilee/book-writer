package sap.ch04

object Alu {
    fun add(a: Int, b: Int): Int = (a + b) and 0xFF
    fun sub(a: Int, b: Int): Int = (a - b) and 0xFF
    fun and(a: Int, b: Int): Int = (a and b) and 0xFF
    fun or(a: Int, b: Int): Int = (a or b) and 0xFF
    fun xor(a: Int, b: Int): Int = (a xor b) and 0xFF
    fun not(a: Int): Int = a.inv() and 0xFF
}
