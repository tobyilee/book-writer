package sap.ch08

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class RegisterFileTest : DescribeSpec({
    describe("RegisterFile") {
        it("A/B/C 3개 레지스터 초기 0") {
            val rf = RegisterFile()
            rf.A.value shouldBe 0
            rf.B.value shouldBe 0
            rf.C.value shouldBe 0
        }
        it("개별 load") {
            val rf = RegisterFile()
            rf.A.load(42)
            rf.A.value shouldBe 42
            rf.B.value shouldBe 0
            rf.C.value shouldBe 0
        }
        it("reset 후 모두 0") {
            val rf = RegisterFile()
            rf.A.load(1); rf.B.load(2); rf.C.load(3)
            rf.reset()
            rf.A.value shouldBe 0
            rf.B.value shouldBe 0
            rf.C.value shouldBe 0
        }
    }
})
