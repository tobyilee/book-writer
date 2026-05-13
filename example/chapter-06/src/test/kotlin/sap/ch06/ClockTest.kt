package sap.ch06

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class ClockTest : DescribeSpec({
    describe("Clock") {
        it("초기 T-state는 1") { Clock().tState shouldBe 1 }
        it("tick 후 T-state 증가") {
            val c = Clock(); c.tick(); c.tState shouldBe 2
        }
        it("T6에서 tick하면 T1으로 wrap") {
            val c = Clock()
            repeat(5) { c.tick() }
            c.tState shouldBe 6
            c.tick()
            c.tState shouldBe 1
        }
        it("reset으로 T1 복귀") {
            val c = Clock()
            c.tick(); c.tick()
            c.reset()
            c.tState shouldBe 1
        }
    }
})
