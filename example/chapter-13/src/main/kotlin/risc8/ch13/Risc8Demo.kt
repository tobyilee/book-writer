package risc8.ch13

fun main() {
    val src = Risc8DemoLocator::class.java.classLoader
        .getResource("programs/fib.risc8")
        ?.readText()
        ?: error("programs/fib.risc8 를 클래스패스에서 찾지 못했다")

    val program = Assembler.assemble(src)
    val cpu = Cpu(program.words)
    cpu.run()

    println("--- RISC-8 Fibonacci ---")
    println("프로그램 워드 수: ${program.words.size}")
    println("실행 사이클 수: ${cpu.cyclesExecuted}")
    val fibs = (0x10..0x19).map { cpu.memory[it] }
    println("메모리 [0x10..0x19] = $fibs")
}

private class Risc8DemoLocator
