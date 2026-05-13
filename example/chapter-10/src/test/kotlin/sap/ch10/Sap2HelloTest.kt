package sap.ch10

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap2HelloTest : DescribeSpec({
    describe("SAP-2 'Hello' 데모") {
        it("Hello\\n 를 port 0에 출력한다") {
            val src = javaClass.classLoader.getResource("programs/hello.sap2")!!.readText()
            val sap2 = assembleAndRun(src)
            sap2.port0Output shouldBe "Hello\n"
        }
    }
})
