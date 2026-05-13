package risc8.ch14

/**
 * 같은 Fibonacci 프로그램을 instruction-accurate / cycle-accurate 두 모델로 돌려
 * 결과(메모리)와 사이클 수를 나란히 비교한다.
 */
fun main() {
    val src = object {}.javaClass.classLoader.getResource("programs/fib.risc8")!!.readText()
    val program = Assembler.assemble(src)

    // Instruction-accurate run (13장 모델)
    val iaCpu = Cpu(program.words)
    iaCpu.run()

    // Cycle-accurate run (14장 모델)
    val caCpu = CycleAccurateCpu(program.words)
    caCpu.run()

    println("--- 같은 Fibonacci, 두 시뮬레이터 ---")
    println("프로그램 워드 수: ${program.words.size}")
    println("instruction-accurate 사이클 (= 실행한 명령어 수): ${iaCpu.cyclesExecuted}")
    println("cycle-accurate 총 사이클: ${caCpu.cycleCount}")
    val cpi = caCpu.cycleCount.toDouble() / iaCpu.cyclesExecuted
    println("평균 CPI(Cycles Per Instruction): %.2f".format(cpi))
    println()
    println("memory[0x10..0x19] (cycle-accurate):")
    println((0x10..0x19).map { caCpu.memory[it] }.joinToString(", "))
    println()
    println("memory[0x10..0x19] (instruction-accurate):")
    println((0x10..0x19).map { iaCpu.memory[it] }.joinToString(", "))
    println()
    println("두 모델은 의미적으로 동일하다 — 다른 건 '몇 사이클 들었는가'뿐이다.")
}
