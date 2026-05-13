package sap.ch10

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap2FibTest : DescribeSpec({
    describe("SAP-2 Fibonacci 데모") {
        it("F0..F9 = 0,1,1,2,3,5,8,13,21,34 를 port 0에 순서대로 출력한다") {
            val src = javaClass.classLoader.getResource("programs/fib.sap2")!!.readText()
            val sap2 = assembleAndRun(src)
            sap2.port0OutputBytes shouldBe listOf(0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        }
    }
})
