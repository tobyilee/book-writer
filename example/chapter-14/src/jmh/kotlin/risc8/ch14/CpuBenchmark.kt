package risc8.ch14

import org.openjdk.jmh.annotations.Benchmark
import org.openjdk.jmh.annotations.BenchmarkMode
import org.openjdk.jmh.annotations.Mode
import org.openjdk.jmh.annotations.OutputTimeUnit
import org.openjdk.jmh.annotations.Scope
import org.openjdk.jmh.annotations.Setup
import org.openjdk.jmh.annotations.State
import java.util.concurrent.TimeUnit

/**
 * JMH 벤치마크 — instruction-accurate vs cycle-accurate 시뮬레이터 처리량을 측정한다.
 *
 * 실행: `./gradlew :chapter-14:jmh`
 *
 * 한 번의 측정은 같은 Fibonacci 프로그램을 통째로 한 번 실행한다 (HALT까지).
 * cycle-accurate 모델이 일반적으로 살짝 느릴 것이다 — 명령어 디코딩이 한 번 더 일어나기 때문.
 * 그러나 두 모델 모두 JIT 컴파일된 Kotlin이라 차이가 크지는 않다.
 */
@State(Scope.Benchmark)
@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
open class CpuBenchmark {
    private lateinit var fibProgram: IntArray

    @Setup
    fun setup() {
        val src = this::class.java.classLoader.getResource("programs/fib.risc8")!!.readText()
        fibProgram = Assembler.assemble(src).words
    }

    @Benchmark
    fun instructionAccurate(): Int {
        val cpu = Cpu(fibProgram)
        cpu.run()
        return cpu.cyclesExecuted
    }

    @Benchmark
    fun cycleAccurate(): Long {
        val cpu = CycleAccurateCpu(fibProgram)
        cpu.run()
        return cpu.cycleCount
    }
}
