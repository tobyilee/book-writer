# 책 동반 예제 코드 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** *코드로 짓는 CPU* 책의 모든 Kotlin 예제를 `example/` 폴더 아래 Gradle Kotlin DSL 멀티모듈 프로젝트로 영구화한다 — 챕터 N 폴더는 챕터 1~N까지의 모든 코드가 누적된 완전 동작 스냅샷.

**Architecture:** 단일 루트 Gradle 프로젝트 + 15개 챕터 subproject. 챕터별로 패키지 네임스페이스가 격리되어(`sap.chXX`, `risc8.chXX`) 누적 정책이 빌드 충돌 없이 성립. kotest 5.x + JUnit5 platform 기반 테스트, JMH는 14장에만 적용.

**Tech Stack:** Kotlin 2.0.20, JVM 17, Gradle 8.7 (wrapper), kotest 5.9.x, JMH 1.37 (`me.champeau.jmh` 0.7.x), application 플러그인.

**스펙 참조:** `docs/superpowers/specs/2026-05-13-example-code-projects-design.md`
**책 본문 참조:** `kotlin-8bit-cpu/chapters/{NN}_final.md` — 각 챕터의 Kotlin 코드 스니펫이 원본 명세이며, 컴파일을 위해 보완이 필요한 import/helper만 추가한다.

---

## File Structure

```
example/
├── .gitignore                       # build/, .gradle/, *.iml 제외
├── settings.gradle.kts              # rootProject + include 15개
├── build.gradle.kts                 # subprojects { kotlin·java·application·test } 공통
├── gradle.properties                # org.gradle.parallel, kotlin.code.style
├── gradle/libs.versions.toml        # kotlin·kotest·jmh 버전 catalog
├── gradle/wrapper/
│   ├── gradle-wrapper.jar
│   └── gradle-wrapper.properties
├── gradlew, gradlew.bat
├── README.md                        # 전체 가이드 + 챕터 매트릭스
├── chapter-01/
│   └── README.md
├── chapter-02/
│   ├── build.gradle.kts             # application { mainClass = "sap.ch02.MiniCpuKt" }
│   ├── README.md
│   └── src/
│       ├── main/kotlin/sap/ch02/MiniCpu.kt
│       └── test/kotlin/sap/ch02/MiniCpuTest.kt
├── chapter-03/
│   ├── build.gradle.kts
│   ├── README.md
│   └── src/main/kotlin/sap/ch03/{Clock.kt, ProgramCounter.kt, Instruction.kt}
│       test/kotlin/sap/ch03/{ClockTest.kt, ProgramCounterTest.kt}
├── chapter-04/
│   └── src/main/kotlin/sap/ch04/{Clock, ProgramCounter, Instruction, Register, Alu}.kt
│       test/kotlin/sap/ch04/{RegisterTest, AluTest}.kt
├── chapter-05/
│   └── src/main/kotlin/sap/ch05/{… ch04 전체 …, AluFlags}.kt
│       test/kotlin/sap/ch05/AluFlagsOverflowSpec.kt   (kotest)
├── chapter-06/
│   ├── build.gradle.kts             # application { mainClass = "sap.ch06.Sap1DemoKt" }
│   └── src/main/kotlin/sap/ch06/{ch05 전체, Ram, Bus, Controller, Sap1, Sap1Demo}.kt
│       test/kotlin/sap/ch06/Sap1IntegrationTest.kt
├── chapter-07/
│   ├── build.gradle.kts             # application { mainClass = "sap.ch07.Asm07DemoKt" }
│   └── src/main/kotlin/sap/ch07/{… ch06 …, asm/{Lexer, Assembler, Disassembler}, Asm07Demo}.kt
│   └── src/main/resources/programs/add.sap1
│       test/kotlin/sap/ch07/{LexerTest, AssemblerTest, AsmEndToEndTest}.kt
├── chapter-08/
│   └── src/main/kotlin/sap/ch08/{ch07 전체, Sap2Core, RegisterFile}.kt
│       test/kotlin/sap/ch08/Sap2CoreTest.kt
├── chapter-09/
│   ├── build.gradle.kts             # application { mainClass = "sap.ch09.HelloDemoKt" }
│   └── src/main/kotlin/sap/ch09/{ch08 …, Jump, Stack, IoPort, HelloDemo, FibDemo}.kt
│   └── src/main/resources/programs/{hello.sap2, fib.sap2}
│       test/kotlin/sap/ch09/{Sap2FibTest, Sap2HelloTest}.kt
├── chapter-10/
│   ├── build.gradle.kts             # application { mainClass = "sap.ch10.DebuggerCliKt" }
│   └── src/main/kotlin/sap/ch10/{ch09 …, MicroRom, Debugger, DebuggerCli}.kt
│       test/kotlin/sap/ch10/{MicroRomTest, DebuggerTest, Sap2TestRomSpec}.kt
├── chapter-11/
│   ├── README.md
│   └── comparison/
│       ├── fib_8080.asm
│       ├── fib_6502.asm
│       ├── fib_z80.asm
│       └── fib_8086.asm
├── chapter-12/
│   └── README.md
├── chapter-13/
│   ├── build.gradle.kts             # application { mainClass = "risc8.ch13.Risc8DemoKt" }
│   └── src/main/kotlin/risc8/ch13/{Isa, Assembler, Cpu, Risc8Demo}.kt
│   └── src/main/resources/programs/fib.risc8
│       test/kotlin/risc8/ch13/{IsaTest, AssemblerTest, CpuFibTest}.kt
├── chapter-14/
│   ├── build.gradle.kts             # application { mainClass = "risc8.ch14.CycleDemoKt" }
│   │                                  + me.champeau.jmh 0.7.x 플러그인
│   └── src/main/kotlin/risc8/ch14/{ch13 …, CycleAccurate, CycleDemo}.kt
│   └── src/jmh/kotlin/risc8/ch14/CpuBenchmark.kt
│       test/kotlin/risc8/ch14/CycleAccurateTest.kt
└── chapter-15/
    └── README.md
```

---

## Task 1: Gradle 루트 골격 (settings + libs catalog + wrapper)

**Files:**
- Create: `example/.gitignore`
- Create: `example/settings.gradle.kts`
- Create: `example/build.gradle.kts`
- Create: `example/gradle.properties`
- Create: `example/gradle/libs.versions.toml`
- Create: `example/gradle/wrapper/gradle-wrapper.properties`
- Create: `example/README.md`

- [ ] **Step 1: 디렉토리 골격 생성**

```bash
cd /Users/tobylee/workspace/ai/book-writer/.claude/worktrees/cpu
mkdir -p example/gradle/wrapper
```

- [ ] **Step 2: `.gitignore` 작성**

```gitignore
# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar

# IntelliJ
.idea/
*.iml
*.ipr
*.iws
out/

# OS
.DS_Store
```

- [ ] **Step 3: `gradle.properties`**

```properties
org.gradle.parallel=true
org.gradle.caching=true
kotlin.code.style=official
```

- [ ] **Step 4: `gradle/libs.versions.toml`**

```toml
[versions]
kotlin = "2.0.20"
kotest = "5.9.1"
jmh-plugin = "0.7.2"

[libraries]
kotest-runner-junit5 = { module = "io.kotest:kotest-runner-junit5", version.ref = "kotest" }
kotest-assertions-core = { module = "io.kotest:kotest-assertions-core", version.ref = "kotest" }
kotest-property = { module = "io.kotest:kotest-property", version.ref = "kotest" }

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
jmh = { id = "me.champeau.jmh", version.ref = "jmh-plugin" }
```

- [ ] **Step 5: `settings.gradle.kts`**

```kotlin
rootProject.name = "kotlin-8bit-cpu-examples"

include(
    "chapter-01",
    "chapter-02",
    "chapter-03",
    "chapter-04",
    "chapter-05",
    "chapter-06",
    "chapter-07",
    "chapter-08",
    "chapter-09",
    "chapter-10",
    "chapter-11",
    "chapter-12",
    "chapter-13",
    "chapter-14",
    "chapter-15",
)
```

- [ ] **Step 6: 루트 `build.gradle.kts` (subproject 공통)**

```kotlin
plugins {
    alias(libs.plugins.kotlin.jvm) apply false
}

subprojects {
    // 코드 챕터에만 Kotlin/test 설정 적용 (README only 챕터는 plugin 안 붙음)
    plugins.withId("org.jetbrains.kotlin.jvm") {
        repositories { mavenCentral() }

        dependencies {
            "testImplementation"(rootProject.libs.kotest.runner.junit5)
            "testImplementation"(rootProject.libs.kotest.assertions.core)
            "testImplementation"(rootProject.libs.kotest.property)
        }

        extensions.configure<org.jetbrains.kotlin.gradle.dsl.KotlinJvmProjectExtension> {
            jvmToolchain(17)
        }

        tasks.withType<Test>().configureEach {
            useJUnitPlatform()
        }
    }
}
```

- [ ] **Step 7: `gradle/wrapper/gradle-wrapper.properties`**

```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.7-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

- [ ] **Step 8: wrapper 스크립트·jar 생성**

기존 Gradle을 갖고 있다면:
```bash
cd example && gradle wrapper --gradle-version 8.7 --distribution-type bin
```
없다면 시스템 임시 디렉토리에 minimal Gradle을 받아 같은 명령 실행, 끝나면 정리.

Expected: `gradlew`, `gradlew.bat`, `gradle/wrapper/gradle-wrapper.jar` 생성.

- [ ] **Step 9: 빌드 검증**

```bash
cd example
./gradlew tasks
```
Expected: 정상 출력, 에러 없음.

- [ ] **Step 10: `README.md`**

다음 내용 포함:
- 책 *코드로 짓는 CPU* 동반 예제임을 명시
- 시작하기 (Kotlin 2.0, JVM 17, `./gradlew build`)
- 챕터 매트릭스 표 — 챕터 번호 / 제목 / 핵심 클래스 / 실행 커맨드
- 누적 스냅샷 정책 한 단락 설명
- 라이선스 (책과 동일 CC BY-NC-SA 4.0)

- [ ] **Step 11: 커밋**

```bash
cd /Users/tobylee/workspace/ai/book-writer/.claude/worktrees/cpu
git add example/.gitignore example/settings.gradle.kts example/build.gradle.kts \
        example/gradle.properties example/gradle/libs.versions.toml \
        example/gradle/wrapper/ example/gradlew example/gradlew.bat \
        example/README.md
git commit -m "Add example/ Gradle multi-module skeleton

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Chapter 1 — README only (코드 없음)

**Files:**
- Create: `example/chapter-01/README.md`

- [ ] **Step 1: README 작성**

다음 섹션 포함:
- 챕터 제목: "1장 — 컴퓨터는 왜 이런 모습인가"
- 한 줄 요지: von Neumann 골격의 정당화
- 챕터 핵심 질문 (책 chapters/01_final.md 첫 문단에서 발췌)
- 학습 지도 (5부 15장 한눈에)
- 코드 없음 명시 + 다음 챕터(2장)의 30줄 미리 보기 — 의사 코드 5~6줄 (책 1장 마지막 절에서 가져옴)

- [ ] **Step 2: 커밋**

```bash
git add example/chapter-01/
git commit -m "Add chapter-01 README (no code chapter)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Chapter 2 — MiniCpu (Kotlin 30줄 미니 CPU)

**책 참조:** `kotlin-8bit-cpu/chapters/02_final.md`

**Files:**
- Create: `example/chapter-02/build.gradle.kts`
- Create: `example/chapter-02/README.md`
- Create: `example/chapter-02/src/main/kotlin/sap/ch02/MiniCpu.kt`
- Create: `example/chapter-02/src/test/kotlin/sap/ch02/MiniCpuTest.kt`

- [ ] **Step 1: `build.gradle.kts`**

```kotlin
plugins {
    alias(libs.plugins.kotlin.jvm)
    application
}

application {
    mainClass.set("sap.ch02.MiniCpuKt")
}
```

- [ ] **Step 2: 테스트 먼저 — `MiniCpuTest.kt`**

```kotlin
package sap.ch02

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class MiniCpuTest : DescribeSpec({
    describe("MiniCpu") {
        it("HLT 단일 명령으로 즉시 정지") {
            val cpu = MiniCpu(memory = intArrayOf(0x10))  // 0x10 = HLT
            cpu.run()
            cpu.halted shouldBe true
            cpu.accumulator shouldBe 0
        }

        it("ADD <addr> 후 HLT 시 누산기에 합산") {
            // 0x01 = ADD opcode (책 chapters/02_final.md)
            // [0]=ADD 3, [1]=HLT, [2]=padding, [3]=42
            val cpu = MiniCpu(memory = intArrayOf(0x01, 3, 0x10, 42))
            cpu.run()
            cpu.accumulator shouldBe 42
        }

        it("두 번의 ADD 누적") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 4, 0x01, 5, 0x10, 10, 20))
            cpu.run()
            cpu.accumulator shouldBe 30
        }

        it("PC가 메모리 끝을 넘으면 즉시 정지") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 1))  // ADD 1, 그 뒤 메모리 없음
            cpu.run()
            cpu.halted shouldBe true
        }

        it("HLT 만나기 전까지 fetch-decode-execute 반복") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 5, 0x01, 6, 0x10, 7, 8))
            cpu.run()
            // 7 + 8 = 15
            cpu.accumulator shouldBe 15
        }

        it("초기 상태에서 PC=0, accumulator=0") {
            val cpu = MiniCpu(memory = intArrayOf(0x10))
            cpu.pc shouldBe 0
            cpu.accumulator shouldBe 0
        }

        it("실행 후 PC가 HLT 다음 위치로 이동") {
            val cpu = MiniCpu(memory = intArrayOf(0x10, 99))
            cpu.run()
            cpu.pc shouldBe 1
        }

        it("ADD 후 PC는 2칸 전진") {
            val cpu = MiniCpu(memory = intArrayOf(0x01, 3, 0x10, 5))
            cpu.run()
            // PC: 0 → 2 (ADD 후) → 3 (HLT 후)
            cpu.pc shouldBe 3
        }
    }
})
```

- [ ] **Step 3: 테스트 실패 확인**

```bash
cd example
./gradlew :chapter-02:test
```
Expected: FAIL, `Unresolved reference: MiniCpu`

- [ ] **Step 4: `MiniCpu.kt` 구현**

책 02_final.md의 코드 블록을 따른다. 다음 시그니처:
```kotlin
package sap.ch02

class MiniCpu(private val memory: IntArray) {
    var pc: Int = 0
        private set
    var accumulator: Int = 0
        private set
    var halted: Boolean = false
        private set

    companion object {
        const val OP_ADD = 0x01
        const val OP_HLT = 0x10
    }

    fun run() {
        while (!halted && pc < memory.size) {
            val opcode = fetch()
            when (opcode) {
                OP_ADD -> { val addr = fetch(); accumulator += memory[addr] }
                OP_HLT -> halted = true
                else -> halted = true  // 알 수 없는 opcode면 정지
            }
        }
    }

    private fun fetch(): Int = memory[pc++]
}

fun main() {
    val program = intArrayOf(0x01, 4, 0x01, 5, 0x10, 17, 25)  // 17 + 25 = 42
    val cpu = MiniCpu(program)
    cpu.run()
    println("Accumulator = ${cpu.accumulator}")
}
```

- [ ] **Step 5: 테스트 통과 확인**

```bash
./gradlew :chapter-02:test
```
Expected: PASS, 8 tests.

- [ ] **Step 6: 데모 실행 확인**

```bash
./gradlew :chapter-02:run
```
Expected: `Accumulator = 42`

- [ ] **Step 7: `README.md` — 챕터 학습 포인트 + 실행 커맨드**

- [ ] **Step 8: 커밋**

```bash
git add example/chapter-02/
git commit -m "Add chapter-02 MiniCpu with 8 tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Chapter 3 — SAP-1 Clock, ProgramCounter, sealed Instruction

**책 참조:** `kotlin-8bit-cpu/chapters/03_final.md`

**Files:**
- Create: `example/chapter-03/build.gradle.kts`
- Create: `example/chapter-03/README.md`
- Create: `example/chapter-03/src/main/kotlin/sap/ch03/Clock.kt`
- Create: `example/chapter-03/src/main/kotlin/sap/ch03/ProgramCounter.kt`
- Create: `example/chapter-03/src/main/kotlin/sap/ch03/Instruction.kt`
- Create: `example/chapter-03/src/test/kotlin/sap/ch03/ClockTest.kt`
- Create: `example/chapter-03/src/test/kotlin/sap/ch03/ProgramCounterTest.kt`

- [ ] **Step 1: `build.gradle.kts`**

```kotlin
plugins {
    alias(libs.plugins.kotlin.jvm)
}
```

(이 챕터는 데모 main 없음, application 플러그인 안 붙임.)

- [ ] **Step 2: `Instruction.kt` — SAP-1 5개 명령의 sealed class**

```kotlin
package sap.ch03

sealed class Instruction(val opcode: Int) {
    data class Lda(val address: Int) : Instruction(0x0)
    data class Add(val address: Int) : Instruction(0x1)
    data class Sub(val address: Int) : Instruction(0x2)
    data object Out : Instruction(0xE)
    data object Hlt : Instruction(0xF)

    companion object {
        fun decode(byte: Int): Instruction {
            val op = (byte shr 4) and 0xF
            val addr = byte and 0xF
            return when (op) {
                0x0 -> Lda(addr)
                0x1 -> Add(addr)
                0x2 -> Sub(addr)
                0xE -> Out
                0xF -> Hlt
                else -> error("Unknown opcode: ${op.toString(16)}")
            }
        }
    }
}
```

- [ ] **Step 3: `ClockTest.kt`**

```kotlin
package sap.ch03

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class ClockTest : DescribeSpec({
    describe("Clock") {
        it("초기 T-state는 1") {
            Clock().tState shouldBe 1
        }
        it("tick 후 T-state 증가") {
            val c = Clock()
            c.tick()
            c.tState shouldBe 2
        }
        it("T6에서 tick하면 T1으로 wrap") {
            val c = Clock()
            repeat(5) { c.tick() }   // T1 → T6
            c.tState shouldBe 6
            c.tick()
            c.tState shouldBe 1
        }
    }
})
```

- [ ] **Step 4: 테스트 실패 확인**

```bash
./gradlew :chapter-03:test
```
Expected: FAIL — `Unresolved reference: Clock`

- [ ] **Step 5: `Clock.kt` 구현**

```kotlin
package sap.ch03

class Clock {
    var tState: Int = 1
        private set

    fun tick() {
        tState = if (tState == 6) 1 else tState + 1
    }
}
```

- [ ] **Step 6: `ProgramCounterTest.kt`**

```kotlin
package sap.ch03

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class ProgramCounterTest : DescribeSpec({
    describe("ProgramCounter (4-bit)") {
        it("초기값 0") {
            ProgramCounter().value shouldBe 0
        }
        it("increment 후 1 증가") {
            val pc = ProgramCounter()
            pc.increment()
            pc.value shouldBe 1
        }
        it("0xF에서 increment하면 wrap 0") {
            val pc = ProgramCounter()
            repeat(15) { pc.increment() }
            pc.value shouldBe 15
            pc.increment()
            pc.value shouldBe 0  // 4-bit wrap
        }
        it("reset으로 0 복귀") {
            val pc = ProgramCounter()
            pc.increment(); pc.increment()
            pc.reset()
            pc.value shouldBe 0
        }
    }
})
```

- [ ] **Step 7: `ProgramCounter.kt` 구현**

```kotlin
package sap.ch03

class ProgramCounter {
    var value: Int = 0
        private set

    fun increment() {
        value = (value + 1) and 0xF  // 4-bit wrap
    }

    fun reset() { value = 0 }
}
```

- [ ] **Step 8: 테스트 통과 확인**

```bash
./gradlew :chapter-03:test
```
Expected: PASS, 7 tests.

- [ ] **Step 9: README + 커밋**

```bash
git add example/chapter-03/
git commit -m "Add chapter-03 SAP-1 Clock/PC/Instruction sealed class

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Chapter 4 — Register, Alu (산술·논리, 플래그 없음)

**책 참조:** `kotlin-8bit-cpu/chapters/04_final.md`

**Files:**
- Create: `example/chapter-04/build.gradle.kts`
- Create: `example/chapter-04/README.md`
- Copy from chapter-03 (패키지 `sap.ch04`로 rename): `Clock.kt`, `ProgramCounter.kt`, `Instruction.kt`
- Create: `example/chapter-04/src/main/kotlin/sap/ch04/Register.kt`
- Create: `example/chapter-04/src/main/kotlin/sap/ch04/Alu.kt`
- Create: `example/chapter-04/src/test/kotlin/sap/ch04/RegisterTest.kt`
- Create: `example/chapter-04/src/test/kotlin/sap/ch04/AluTest.kt`

- [ ] **Step 1: chapter-03 코드 복사 + 패키지 rename**

```bash
cd example
mkdir -p chapter-04/src/main/kotlin/sap/ch04
cp chapter-03/src/main/kotlin/sap/ch03/*.kt chapter-04/src/main/kotlin/sap/ch04/
sed -i '' 's/package sap\.ch03/package sap.ch04/g' chapter-04/src/main/kotlin/sap/ch04/*.kt
```

기존 ClockTest, ProgramCounterTest도 같은 방식으로 복사·rename.

- [ ] **Step 2: `RegisterTest.kt` 작성**

```kotlin
package sap.ch04

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class RegisterTest : DescribeSpec({
    describe("Register (8-bit)") {
        it("초기값 0") { Register().value shouldBe 0 }
        it("load 후 값 보유") {
            val r = Register(); r.load(42); r.value shouldBe 42
        }
        it("0xFF 넘는 값은 마스킹") {
            val r = Register(); r.load(0x123); r.value shouldBe 0x23
        }
        it("음수는 2의 보수 8비트로 마스킹") {
            val r = Register(); r.load(-1); r.value shouldBe 0xFF
        }
        it("clear로 0 복귀") {
            val r = Register(); r.load(99); r.clear(); r.value shouldBe 0
        }
    }
})
```

- [ ] **Step 3: `Register.kt` 구현**

```kotlin
package sap.ch04

class Register {
    var value: Int = 0
        private set

    fun load(v: Int) { value = v and 0xFF }
    fun clear() { value = 0 }
}
```

- [ ] **Step 4: `AluTest.kt` — 산술·논리 (플래그 없음)**

```kotlin
package sap.ch04

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import io.kotest.data.forAll
import io.kotest.data.row

class AluTest : DescribeSpec({
    describe("Alu 산술") {
        it("ADD") {
            Alu.add(10, 20) shouldBe 30
            Alu.add(255, 1) shouldBe 0  // 8비트 wrap
            Alu.add(0, 0) shouldBe 0
        }
        it("SUB") {
            Alu.sub(50, 10) shouldBe 40
            Alu.sub(0, 1) shouldBe 0xFF
        }
        it("산술 표 기반 검증") {
            forAll(
                row(0, 0, 0),
                row(1, 1, 2),
                row(127, 1, 128),
                row(255, 255, 254),
                row(100, 200, 44),  // 300 mod 256
            ) { a, b, expected -> Alu.add(a, b) shouldBe expected }
        }
    }
    describe("Alu 논리") {
        it("AND") { Alu.and(0b11110000, 0b10101010) shouldBe 0b10100000 }
        it("OR") { Alu.or(0b11110000, 0b00001111) shouldBe 0xFF }
        it("XOR") { Alu.xor(0xFF, 0x0F) shouldBe 0xF0 }
        it("NOT") { Alu.not(0x00) shouldBe 0xFF; Alu.not(0xFF) shouldBe 0x00 }
    }
})
```

- [ ] **Step 5: `Alu.kt` 구현**

```kotlin
package sap.ch04

object Alu {
    fun add(a: Int, b: Int): Int = (a + b) and 0xFF
    fun sub(a: Int, b: Int): Int = (a - b) and 0xFF
    fun and(a: Int, b: Int): Int = (a and b) and 0xFF
    fun or(a: Int, b: Int): Int = (a or b) and 0xFF
    fun xor(a: Int, b: Int): Int = (a xor b) and 0xFF
    fun not(a: Int): Int = a.inv() and 0xFF
}
```

- [ ] **Step 6: 테스트 통과 확인**

```bash
./gradlew :chapter-04:test
```
Expected: PASS — Clock, ProgramCounter, Register, Alu 합쳐 ~20 테스트.

- [ ] **Step 7: README + 커밋**

```bash
git add example/chapter-04/
git commit -m "Add chapter-04 SAP-1 Register + Alu (no flags yet)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Chapter 5 — AluFlags (Z/C/S/V) + 256x2 overflow 테이블

**책 참조:** `kotlin-8bit-cpu/chapters/05_final.md` — 입문자의 무덤 정면돌파 챕터.

**Files:**
- Create: `example/chapter-05/build.gradle.kts`, `README.md`
- Copy from chapter-04 (rename ch04 → ch05): all `*.kt` (Clock, ProgramCounter, Instruction, Register)
- Create: `example/chapter-05/src/main/kotlin/sap/ch05/AluFlags.kt` — 플래그 포함 ALU
- Create: `example/chapter-05/src/test/kotlin/sap/ch05/AluFlagsOverflowSpec.kt` — kotest property-based

- [ ] **Step 1: chapter-04 코드 복사 + rename (Alu.kt 제외)**

```bash
cd example
mkdir -p chapter-05/src/main/kotlin/sap/ch05
cp chapter-04/src/main/kotlin/sap/ch04/{Clock,ProgramCounter,Instruction,Register}.kt chapter-05/src/main/kotlin/sap/ch05/
sed -i '' 's/package sap\.ch04/package sap.ch05/g' chapter-05/src/main/kotlin/sap/ch05/*.kt
```

테스트도 같은 방식 복사 + rename.

- [ ] **Step 2: `AluFlagsOverflowSpec.kt` — kotest forAll 표 기반**

```kotlin
package sap.ch05

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class AluFlagsOverflowSpec : DescribeSpec({
    describe("AluFlags.add — 모든 256x256 조합 검증") {
        it("결과는 (a+b) mod 256") {
            for (a in 0..255) for (b in 0..255) {
                val r = AluFlags.add(a, b)
                r.value shouldBe ((a + b) and 0xFF)
            }
        }
        it("Carry 플래그는 a+b >= 256일 때만 1") {
            for (a in 0..255) for (b in 0..255) {
                val r = AluFlags.add(a, b)
                r.carry shouldBe ((a + b) >= 256)
            }
        }
        it("Zero 플래그는 결과가 0일 때만 1") {
            for (a in 0..255) for (b in 0..255) {
                val r = AluFlags.add(a, b)
                r.zero shouldBe (((a + b) and 0xFF) == 0)
            }
        }
        it("Sign 플래그는 결과 비트7이 1일 때만 1") {
            for (a in 0..255) for (b in 0..255) {
                val r = AluFlags.add(a, b)
                r.sign shouldBe (((a + b) and 0x80) != 0)
            }
        }
        it("Overflow 플래그는 부호 있는 overflow가 발생할 때만 1") {
            // signed: a, b를 부호 있는 8비트로 해석
            for (a in 0..255) for (b in 0..255) {
                val r = AluFlags.add(a, b)
                val signedA = a.toByte().toInt()
                val signedB = b.toByte().toInt()
                val signedSum = signedA + signedB
                val overflow = signedSum < -128 || signedSum > 127
                r.overflow shouldBe overflow
            }
        }
    }
    describe("AluFlags.sub — 256x256 조합") {
        it("ADC/SBC overflow 검증") {
            for (a in 0..255) for (b in 0..255) {
                val r = AluFlags.sub(a, b)
                r.value shouldBe ((a - b) and 0xFF)
                r.carry shouldBe (a >= b)   // SBC 관습: borrow=0 이면 carry=1
                val signedA = a.toByte().toInt()
                val signedB = b.toByte().toInt()
                val signedDiff = signedA - signedB
                val overflow = signedDiff < -128 || signedDiff > 127
                r.overflow shouldBe overflow
            }
        }
    }
})
```

- [ ] **Step 3: `AluFlags.kt` 구현**

```kotlin
package sap.ch05

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
        return AluResult(
            value = v,
            zero = v == 0,
            carry = full >= 256,
            sign = (v and 0x80) != 0,
            overflow = run {
                val sa = a.toByte().toInt()
                val sb = b.toByte().toInt()
                val ss = sa + sb
                ss < -128 || ss > 127
            },
        )
    }

    fun sub(a: Int, b: Int): AluResult {
        val full = a - b
        val v = full and 0xFF
        return AluResult(
            value = v,
            zero = v == 0,
            carry = a >= b,
            sign = (v and 0x80) != 0,
            overflow = run {
                val sa = a.toByte().toInt()
                val sb = b.toByte().toInt()
                val ss = sa - sb
                ss < -128 || ss > 127
            },
        )
    }
}
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
./gradlew :chapter-05:test
```
Expected: PASS — 256×256×2 = 131,072 ALU 검증 통과.

- [ ] **Step 5: README + 커밋**

README에 "이 챕터의 핵심: overflow 무덤을 표 기반 테스트로 잡는다"를 강조.

```bash
git add example/chapter-05/
git commit -m "Add chapter-05 AluFlags with 131k case overflow validation

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Chapter 6 — RAM, Bus, Controller, full Sap1 (5바이트 프로그램 실행)

**책 참조:** `kotlin-8bit-cpu/chapters/06_final.md`

**Files:**
- Create: `example/chapter-06/build.gradle.kts`, `README.md`
- Copy from chapter-05 (rename ch05 → ch06): all `*.kt`. AluFlags → Alu로 이름 통일 (sap.ch06.Alu).
- Create: `example/chapter-06/src/main/kotlin/sap/ch06/Ram.kt` — 16바이트
- Create: `example/chapter-06/src/main/kotlin/sap/ch06/Bus.kt` — W-bus
- Create: `example/chapter-06/src/main/kotlin/sap/ch06/Controller.kt` — 하드와이어드 시퀀서 (T1~T6)
- Create: `example/chapter-06/src/main/kotlin/sap/ch06/Sap1.kt` — 모든 모듈 통합
- Create: `example/chapter-06/src/main/kotlin/sap/ch06/Sap1Demo.kt` — main, 5바이트 프로그램 실행
- Create: `example/chapter-06/src/test/kotlin/sap/ch06/Sap1IntegrationTest.kt`

- [ ] **Step 1: chapter-05 코드 복사 + 패키지 rename**

같은 패턴. AluFlags 코드는 그대로 가져오되 본 챕터 컨벤션에 맞게 `Alu`로 사용. (책에서는 5장에서 ALU가 완성되어 6장은 그대로 활용.)

- [ ] **Step 2: 테스트 먼저 — `Sap1IntegrationTest.kt`**

```kotlin
package sap.ch06

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap1IntegrationTest : DescribeSpec({
    describe("SAP-1 통합 실행") {
        it("LDA 9 → ADD A → OUT → HLT 가 메모리[9] 값을 출력") {
            // 메모리 16바이트:
            // [0] LDA 9  = 0x09
            // [1] ADD A  = 0x1A
            // [2] OUT    = 0xE0
            // [3] HLT    = 0xF0
            // [9] 0x2A (42)
            // [A] 0x05 (5)
            val rom = IntArray(16).apply {
                this[0] = 0x09
                this[1] = 0x1A
                this[2] = 0xE0
                this[3] = 0xF0
                this[9] = 0x2A
                this[10] = 0x05
            }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.output shouldBe 0x2F   // 0x2A + 0x05 = 0x2F (47)
            sap1.halted shouldBe true
        }
        it("HLT 단독으로 즉시 정지") {
            val rom = IntArray(16).apply { this[0] = 0xF0 }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.halted shouldBe true
        }
        it("SUB 명령") {
            // LDA 9 (10) → SUB A (5) → OUT → HLT
            val rom = IntArray(16).apply {
                this[0] = 0x09
                this[1] = 0x2A
                this[2] = 0xE0
                this[3] = 0xF0
                this[9] = 0x0A
                this[10] = 0x05
            }
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.output shouldBe 0x05
        }
        // ... (총 15개 이상의 통합·단위 테스트, 책 06_final.md의 테스트 항목 참조)
    }
})
```

- [ ] **Step 3: 구현 — 책 chapters/06_final.md의 Ram·Bus·Controller·Sap1 코드를 따른다**

핵심 클래스 시그니처:

```kotlin
// Ram.kt
package sap.ch06
class Ram(initial: IntArray) {
    private val mem = IntArray(16).also { initial.copyInto(it) }
    fun read(addr: Int): Int = mem[addr and 0xF]
    fun write(addr: Int, value: Int) { mem[addr and 0xF] = value and 0xFF }
}

// Bus.kt
package sap.ch06
class Bus { var value: Int = 0 }   // 8-bit W-bus

// Controller.kt — T1~T6 하드와이어드
package sap.ch06
class Controller {
    fun controlSignalsFor(opcode: Int, tState: Int): Set<ControlSignal> = ...
}
enum class ControlSignal { Ep, Lm, Cp, Er, Li, Ei, La, Ea, Su, Eu, Lb, Lo, Eo, Hlt, ... }

// Sap1.kt — 모듈 통합
package sap.ch06
class Sap1(rom: IntArray) {
    private val pc = ProgramCounter()
    private val ram = Ram(rom)
    private val a = Register()
    private val b = Register()
    private val ir = Register()
    private val out = Register()
    private val bus = Bus()
    private val ctrl = Controller()
    var output: Int = 0; private set
    var halted: Boolean = false; private set

    fun run() {
        while (!halted) { step() }
    }
    private fun step() { /* T1~T6 사이클 */ }
}
```

본문 구현은 책 06_final.md의 코드 블록을 그대로 옮기되, 컴파일을 위해 누락된 helper나 import를 채운다.

- [ ] **Step 4: 데모 — `Sap1Demo.kt`**

```kotlin
package sap.ch06

fun main() {
    val rom = IntArray(16).apply {
        this[0] = 0x09
        this[1] = 0x1A
        this[2] = 0xE0
        this[3] = 0xF0
        this[9] = 0x2A
        this[10] = 0x05
    }
    val sap1 = Sap1(rom)
    sap1.run()
    println("OUT = ${sap1.output}")
}
```

- [ ] **Step 5: `build.gradle.kts`**

```kotlin
plugins {
    alias(libs.plugins.kotlin.jvm)
    application
}
application { mainClass.set("sap.ch06.Sap1DemoKt") }
```

- [ ] **Step 6: 테스트 통과 + 데모 실행 검증**

```bash
./gradlew :chapter-06:test
./gradlew :chapter-06:run
```
Expected: 테스트 모두 통과 + 데모 출력 `OUT = 47` (또는 `0x2F`).

- [ ] **Step 7: README + 커밋**

```bash
git add example/chapter-06/
git commit -m "Add chapter-06 SAP-1 integrated (LDA→ADD→OUT→HLT runs)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: Chapter 7 — Lexer, Assembler, Disassembler (e2e 어셈블→실행)

**책 참조:** `kotlin-8bit-cpu/chapters/07_final.md`

**Files:**
- Create: `example/chapter-07/build.gradle.kts`, `README.md`
- Copy from chapter-06 (rename to ch07): RAM, Bus, Controller, Sap1, Register, Alu, Clock, ProgramCounter, Instruction
- Create: `example/chapter-07/src/main/kotlin/sap/ch07/asm/Lexer.kt`
- Create: `example/chapter-07/src/main/kotlin/sap/ch07/asm/Assembler.kt`
- Create: `example/chapter-07/src/main/kotlin/sap/ch07/asm/Disassembler.kt`
- Create: `example/chapter-07/src/main/kotlin/sap/ch07/Asm07Demo.kt`
- Create: `example/chapter-07/src/main/resources/programs/add.sap1`
- Create: `example/chapter-07/src/test/kotlin/sap/ch07/LexerTest.kt`
- Create: `example/chapter-07/src/test/kotlin/sap/ch07/AssemblerTest.kt`
- Create: `example/chapter-07/src/test/kotlin/sap/ch07/AsmEndToEndTest.kt`

- [ ] **Step 1: chapter-06 복사 + rename**

- [ ] **Step 2: 어셈블리 프로그램 `programs/add.sap1`**

```
; SAP-1 program: add 42 + 5, print result
start:  LDA  9        ; load mem[9] into A
        ADD  A        ; A = A + mem[10]
        OUT           ; print A
        HLT
9:      $2A           ; 42 (literal at addr 9)
A:      $05           ; 5  (literal at addr 10)
```

- [ ] **Step 3: 테스트 먼저 — `LexerTest.kt`**

```kotlin
package sap.ch07

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import sap.ch07.asm.Lexer
import sap.ch07.asm.Token

class LexerTest : DescribeSpec({
    describe("Lexer") {
        it("주석은 무시한다") {
            Lexer.tokenize("; this is a comment\nLDA 9") shouldBe listOf(
                Token.Mnemonic("LDA"), Token.Number(9),
            )
        }
        it("라벨 인식") {
            Lexer.tokenize("start: LDA 9").let {
                it[0] shouldBe Token.Label("start")
                it[1] shouldBe Token.Mnemonic("LDA")
            }
        }
        it("\$로 시작하는 hex 리터럴") {
            Lexer.tokenize("\$2A") shouldBe listOf(Token.Number(0x2A))
        }
    }
})
```

- [ ] **Step 4: 테스트 먼저 — `AssemblerTest.kt`**

```kotlin
package sap.ch07

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import sap.ch07.asm.Assembler

class AssemblerTest : DescribeSpec({
    describe("Assembler 2-pass") {
        it("심볼 테이블에 라벨이 들어간다") {
            val asm = Assembler.assemble("""
                start: LDA 9
                       HLT
            """.trimIndent())
            asm.symbols["start"] shouldBe 0
        }
        it("출력 바이트열이 정확하다") {
            val asm = Assembler.assemble("LDA 9\nADD A\nOUT\nHLT")
            asm.bytes.toList() shouldBe listOf(0x09, 0x1A, 0xE0, 0xF0)
        }
    }
})
```

- [ ] **Step 5: 테스트 먼저 — `AsmEndToEndTest.kt`**

```kotlin
package sap.ch07

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import sap.ch07.asm.Assembler

class AsmEndToEndTest : DescribeSpec({
    describe("어셈블 → SAP-1 실행") {
        it("add.sap1을 어셈블하고 실행하면 OUT=47") {
            val src = javaClass.getResource("/programs/add.sap1")!!.readText()
            val asm = Assembler.assemble(src)
            val rom = IntArray(16)
            asm.bytes.copyInto(rom)
            val sap1 = Sap1(rom)
            sap1.run()
            sap1.output shouldBe 47
        }
    }
})
```

- [ ] **Step 6: 구현 — `Lexer`, `Assembler`, `Disassembler`**

책 07_final.md의 코드 블록을 따른다. `sealed class Token`(Label/Mnemonic/Number), 2-pass `Assembler`, `Disassembler.bytesToText(bytes)`.

- [ ] **Step 7: `Asm07Demo.kt` (main)**

```kotlin
package sap.ch07
import sap.ch07.asm.Assembler

fun main() {
    val src = object {}.javaClass.getResource("/programs/add.sap1")!!.readText()
    val asm = Assembler.assemble(src)
    val rom = IntArray(16).also { asm.bytes.copyInto(it) }
    val sap1 = Sap1(rom)
    sap1.run()
    println("어셈블 → 실행 → OUT = ${sap1.output}")
}
```

- [ ] **Step 8: 테스트 통과 + 데모 실행 검증**

```bash
./gradlew :chapter-07:test
./gradlew :chapter-07:run
```
Expected: 테스트 통과, 데모는 `OUT = 47` 출력.

- [ ] **Step 9: README + 커밋**

```bash
git add example/chapter-07/
git commit -m "Add chapter-07 SAP-1 assembler/disassembler (e2e source→exec)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: Chapter 8 — SAP-2 scaffold (64KB RAM, 16-bit PC, A/B/C 레지스터)

**책 참조:** `kotlin-8bit-cpu/chapters/08_final.md`

**Files:**
- Create: `example/chapter-08/build.gradle.kts`, `README.md`
- Copy from chapter-07 (rename to ch08): SAP-1 전체 (다음 챕터들에서 SAP-2가 SAP-1을 대체하지 않고 별도로 짖는다 — 같은 패키지에 공존 가능)
- Create: `example/chapter-08/src/main/kotlin/sap/ch08/Sap2Core.kt`
- Create: `example/chapter-08/src/main/kotlin/sap/ch08/RegisterFile.kt`
- Create: `example/chapter-08/src/test/kotlin/sap/ch08/Sap2CoreTest.kt`

- [ ] **Step 1: chapter-07 코드 복사 + rename**

- [ ] **Step 2: 테스트 — `Sap2CoreTest.kt`**

```kotlin
package sap.ch08

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap2CoreTest : DescribeSpec({
    describe("Sap2Core") {
        it("64KB 메모리 + 16비트 PC") {
            val core = Sap2Core()
            core.memory.size shouldBe 65536
            core.pc shouldBe 0
        }
        it("PC가 0xFFFF에서 wrap") {
            val core = Sap2Core()
            core.setPc(0xFFFF)
            core.incrementPc()
            core.pc shouldBe 0
        }
    }
    describe("RegisterFile") {
        it("A/B/C 3개 레지스터") {
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
        }
    }
})
```

- [ ] **Step 3: 구현**

```kotlin
// Sap2Core.kt
package sap.ch08
class Sap2Core {
    val memory = IntArray(65536)
    var pc: Int = 0
        private set
    fun setPc(v: Int) { pc = v and 0xFFFF }
    fun incrementPc() { pc = (pc + 1) and 0xFFFF }
    fun fetch(): Int { val b = memory[pc]; incrementPc(); return b }
}

// RegisterFile.kt
package sap.ch08
class RegisterFile {
    val A = Register()
    val B = Register()
    val C = Register()
}
```

- [ ] **Step 4: 테스트 통과 + 커밋**

```bash
./gradlew :chapter-08:test
git add example/chapter-08/
git commit -m "Add chapter-08 SAP-2 scaffold (64KB, 16-bit PC, A/B/C regs)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 10: Chapter 9 — Jump, Stack, IoPort, Fibonacci + "Hello"

**책 참조:** `kotlin-8bit-cpu/chapters/09_final.md`

**Files:**
- Create: `example/chapter-09/build.gradle.kts`, `README.md`
- Copy from chapter-08 (rename to ch09)
- Create: `example/chapter-09/src/main/kotlin/sap/ch09/Jump.kt` — 분기 명령
- Create: `example/chapter-09/src/main/kotlin/sap/ch09/Stack.kt` — SP, push/pop, CALL/RET
- Create: `example/chapter-09/src/main/kotlin/sap/ch09/IoPort.kt` — IN/OUT 포트
- Create: `example/chapter-09/src/main/kotlin/sap/ch09/Sap2.kt` — 전체 통합 (SAP-2 풀)
- Create: `example/chapter-09/src/main/kotlin/sap/ch09/HelloDemo.kt`
- Create: `example/chapter-09/src/main/kotlin/sap/ch09/FibDemo.kt`
- Create: `example/chapter-09/src/main/resources/programs/{hello.sap2, fib.sap2}`
- Create: `example/chapter-09/src/test/kotlin/sap/ch09/{Sap2FibTest, Sap2HelloTest}.kt`

- [ ] **Step 1: chapter-08 복사 + rename**

- [ ] **Step 2: 어셈블리 프로그램**

`hello.sap2`:
```
; Hello, World! 출력
        LDI A, 'H'
        OUT 0          ; port 0 = ASCII output
        LDI A, 'e'
        OUT 0
        ; ...
        HLT
```

`fib.sap2`:
```
; Fibonacci 처음 10개 출력
        LDI A, 0
        LDI B, 1
        LDI C, 10
loop:   OUT 0          ; print A
        MOV D, A
        ADD A, B
        MOV B, D
        DEC C
        JNZ loop
        HLT
```

- [ ] **Step 3: 테스트 먼저 — `Sap2HelloTest.kt`**

```kotlin
package sap.ch09

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap2HelloTest : DescribeSpec({
    describe("SAP-2 'Hello'") {
        it("Hello, World! 를 port 0에 출력") {
            val src = javaClass.getResource("/programs/hello.sap2")!!.readText()
            val sap2 = assembleAndRun(src)
            sap2.port0Output shouldBe "Hello, World!\n"
        }
    }
})
```

- [ ] **Step 4: 테스트 먼저 — `Sap2FibTest.kt`**

```kotlin
package sap.ch09

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap2FibTest : DescribeSpec({
    describe("SAP-2 Fibonacci") {
        it("처음 10개 Fibonacci 출력 (0,1,1,2,3,5,8,13,21,34)") {
            val src = javaClass.getResource("/programs/fib.sap2")!!.readText()
            val sap2 = assembleAndRun(src)
            sap2.port0OutputBytes shouldBe listOf(0,1,1,2,3,5,8,13,21,34)
        }
    }
})
```

- [ ] **Step 5: 구현 — Jump, Stack, IoPort, Sap2**

책 09_final.md의 코드를 따른다. 핵심:
- `JZ/JNZ/JM addr16` — flag 기반 분기
- `Stack` — SP는 16비트, 메모리 영역 사용 (SAP-2 명세대로)
- `CALL addr16` — return address push 후 점프
- `RET` — pop 후 점프
- `IoPort` — 16개 input port + 16개 output port (책 명세)
- `Sap2` — Sap1과 별도 클래스로, 모든 모듈 통합

어셈블러는 chapter-07의 `sap.ch09.asm.Assembler`를 SAP-2 명령으로 확장. 새 명령: LDI, MOV, JZ, JNZ, JM, CALL, RET, IN, OUT, INC, DEC.

helper: `fun assembleAndRun(src: String): Sap2 { … }`

- [ ] **Step 6: 데모 main들**

```kotlin
package sap.ch09
fun main() {
    val src = object {}.javaClass.getResource("/programs/hello.sap2")!!.readText()
    val sap2 = assembleAndRun(src)
    print(sap2.port0Output)
}
```

`build.gradle.kts`:
```kotlin
application { mainClass.set("sap.ch09.HelloDemoKt") }
```

- [ ] **Step 7: 테스트 통과 + 데모 실행**

```bash
./gradlew :chapter-09:test
./gradlew :chapter-09:run
```
Expected: 테스트 통과 + 데모 출력 `Hello, World!`.

- [ ] **Step 8: 커밋**

```bash
git add example/chapter-09/
git commit -m "Add chapter-09 SAP-2 branch/stack/IO (Hello + Fibonacci demos)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 11: Chapter 10 — MicroRom, Debugger, SAP-2 test ROM

**책 참조:** `kotlin-8bit-cpu/chapters/10_final.md`

**Files:**
- Create: `example/chapter-10/build.gradle.kts`, `README.md`
- Copy from chapter-09 (rename to ch10) — 단, Controller를 마이크로코드 ROM 기반으로 교체
- Create: `example/chapter-10/src/main/kotlin/sap/ch10/MicroRom.kt` — control matrix (35 signals × 10 T-states)
- Create: `example/chapter-10/src/main/kotlin/sap/ch10/Debugger.kt` — breakpoint/step/dump
- Create: `example/chapter-10/src/main/kotlin/sap/ch10/DebuggerCli.kt` — CLI
- Create: `example/chapter-10/src/test/kotlin/sap/ch10/{MicroRomTest, DebuggerTest, Sap2TestRomSpec}.kt`

- [ ] **Step 1: chapter-09 복사 + rename + Controller 제거 (MicroRom으로 대체)**

- [ ] **Step 2: 테스트 — `MicroRomTest.kt`**

```kotlin
package sap.ch10
import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import io.kotest.matchers.collections.shouldContain

class MicroRomTest : DescribeSpec({
    describe("MicroRom") {
        it("LDA 명령의 T1에서 PC→MAR 신호 발생") {
            val signals = MicroRom.signalsFor(opcode = Opcodes.LDA, tState = 1)
            signals shouldContain ControlSignal.PC_TO_MAR
        }
        it("HLT 명령은 T4 즉시 정지 신호") {
            val signals = MicroRom.signalsFor(opcode = Opcodes.HLT, tState = 4)
            signals shouldContain ControlSignal.HALT
        }
        // ...
    }
})
```

- [ ] **Step 3: 테스트 — `DebuggerTest.kt`**

```kotlin
package sap.ch10
import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class DebuggerTest : DescribeSpec({
    describe("Debugger") {
        it("breakpoint에서 정지") {
            val dbg = Debugger(buildSap2WithFibProgram())
            dbg.setBreakpoint(0x10)
            dbg.continueUntilBreak()
            dbg.cpu.pc shouldBe 0x10
        }
        it("step 한 번이 PC를 한 명령 진행") {
            val dbg = Debugger(buildSap2WithFibProgram())
            val pcBefore = dbg.cpu.pc
            dbg.step()
            dbg.cpu.pc shouldBe (pcBefore + lengthOf(currentOpcode))
        }
        it("registerDump이 A/B/C/SP/PC 모두 포함") {
            val dump = Debugger(buildSap2WithFibProgram()).registerDump()
            dump shouldContain "A="
            dump shouldContain "B="
            dump shouldContain "C="
            dump shouldContain "PC="
        }
    }
})
```

- [ ] **Step 4: 테스트 — `Sap2TestRomSpec.kt` (회귀 검증)**

```kotlin
package sap.ch10
import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class Sap2TestRomSpec : DescribeSpec({
    describe("SAP-2 test ROM (6502 functional test의 SAP-2 축소판)") {
        it("산술 명령 묶음 통과") {
            val rom = loadTestRom("arithmetic")
            val sap2 = runRom(rom)
            sap2.testRomResult shouldBe TestResult.PASS
        }
        it("분기 명령 묶음 통과") {
            val rom = loadTestRom("branch")
            val sap2 = runRom(rom)
            sap2.testRomResult shouldBe TestResult.PASS
        }
        it("스택 명령 묶음 통과") {
            val rom = loadTestRom("stack")
            val sap2 = runRom(rom)
            sap2.testRomResult shouldBe TestResult.PASS
        }
    }
})
```

- [ ] **Step 5: 구현 — MicroRom + Debugger + DebuggerCli**

책 10_final.md의 코드를 따른다.
- `enum class ControlSignal { Ep, Lm, Cp, Er, Li, Ei, La, Ea, Su, Eu, Lb, Lo, Eo, Halt, ... }`
- `object MicroRom { fun signalsFor(opcode: Int, tState: Int): Set<ControlSignal> = ... }`
- `class Debugger(val cpu: Sap2) { fun setBreakpoint, step, continueUntilBreak, registerDump, memoryDump }`
- `DebuggerCli` — `main`이 stdin 명령(`b 10`, `s`, `c`, `r`, `q`) 처리

- [ ] **Step 6: build.gradle.kts**

```kotlin
plugins { alias(libs.plugins.kotlin.jvm); application }
application { mainClass.set("sap.ch10.DebuggerCliKt") }
```

- [ ] **Step 7: 테스트 통과**

```bash
./gradlew :chapter-10:test
```

- [ ] **Step 8: 커밋**

```bash
git add example/chapter-10/
git commit -m "Add chapter-10 SAP-2 microcode ROM + debugger + test ROM

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 12: Chapter 11 — asm 4개 + README (Kotlin 없음)

**Files:**
- Create: `example/chapter-11/README.md`
- Create: `example/chapter-11/comparison/fib_8080.asm`
- Create: `example/chapter-11/comparison/fib_6502.asm`
- Create: `example/chapter-11/comparison/fib_z80.asm`
- Create: `example/chapter-11/comparison/fib_8086.asm`

- [ ] **Step 1: 책 11장에서 4개 어셈블리 추출**

`kotlin-8bit-cpu/chapters/11_final.md`에 같은 Fibonacci 알고리즘이 네 어셈블리로 들어 있다. 그대로 옮긴다.

각 파일 첫 줄에 주석 4~5줄로 어떤 CPU·문법인지 명시.

- [ ] **Step 2: README — 비교 표**

다음 포함:
- 같은 Fibonacci, 네 어셈블리
- 4개 CPU 정량 비교 표 (트랜지스터·레지스터·명령어·어드레싱·가격)
- I/O 모델 (memory-mapped vs 별도 포트)
- 본 책 SAP-2가 8080의 직계 후예라는 회수

- [ ] **Step 3: 커밋**

```bash
git add example/chapter-11/
git commit -m "Add chapter-11 four-CPU Fibonacci comparison (asm files)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 13: Chapter 12 — README only (RISC vs CISC 역사)

**Files:**
- Create: `example/chapter-12/README.md`

- [ ] **Step 1: README 작성**

책 12장 핵심: RISC 1980년대 논쟁 정리. README에는 한 페이지짜리 요약 + 책 §4.1 인용 + 다음 챕터(13장 RISC-8 ISA 설계)로 가는 다리.

- [ ] **Step 2: 커밋**

```bash
git add example/chapter-12/
git commit -m "Add chapter-12 RISC-vs-CISC history (README only)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 14: Chapter 13 — RISC-8 ISA, Assembler, CPU (Fibonacci 동작)

**책 참조:** `kotlin-8bit-cpu/chapters/13_final.md` — 책의 가장 창의적 산물.

**Files:**
- Create: `example/chapter-13/build.gradle.kts`, `README.md`
- Create: `example/chapter-13/src/main/kotlin/risc8/ch13/Isa.kt` — sealed class Instruction, R/I/J-type 인코딩
- Create: `example/chapter-13/src/main/kotlin/risc8/ch13/Assembler.kt` — RISC-8 어셈블러
- Create: `example/chapter-13/src/main/kotlin/risc8/ch13/Cpu.kt` — 16개 레지스터, load/store, branch, JAL/JR
- Create: `example/chapter-13/src/main/kotlin/risc8/ch13/Risc8Demo.kt`
- Create: `example/chapter-13/src/main/resources/programs/fib.risc8`
- Create: `example/chapter-13/src/test/kotlin/risc8/ch13/{IsaTest, AssemblerTest, CpuFibTest}.kt`

- [ ] **Step 1: 새 출발 — chapter-12 폴더에는 코드가 없으니 chapter-13은 from-scratch**

```bash
mkdir -p example/chapter-13/src/main/kotlin/risc8/ch13
mkdir -p example/chapter-13/src/main/resources/programs
mkdir -p example/chapter-13/src/test/kotlin/risc8/ch13
```

- [ ] **Step 2: ISA 명세 inline in README**

README에 본 책 RISC-8 ISA 명세:
- 16비트 고정 길이 명령어
- R-type: 7비트 opcode + 3비트 rd + 3비트 rs1 + 3비트 rs2 (총 16비트)
- I-type: 7비트 opcode + 3비트 rd + 3비트 rs1 + 3비트 immediate
- J-type: 7비트 opcode + 9비트 offset
- 16개 레지스터 (R0=zero, R1~R15)
- 명령어: ADD, SUB, AND, OR, XOR, SHL, SHR, LDB, STB, BEQ, BNE, JAL, JR, ECALL, EBREAK
- 단일 trap vector + cause register (인터럽트)

- [ ] **Step 3: 테스트 먼저 — `IsaTest.kt`**

```kotlin
package risc8.ch13
import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class IsaTest : DescribeSpec({
    describe("RISC-8 명령어 인코딩") {
        it("ADD R1, R2, R3 인코딩") {
            val instr = Instruction.Add(rd = 1, rs1 = 2, rs2 = 3)
            instr.encode() shouldBe 0b0000001_001_010_011  // 7+3+3+3 = 16
        }
        it("디코딩 round-trip") {
            val original = Instruction.Add(rd = 1, rs1 = 2, rs2 = 3)
            val decoded = Instruction.decode(original.encode())
            decoded shouldBe original
        }
        it("BEQ는 J-type") {
            val instr = Instruction.Beq(offset = 8)
            val decoded = Instruction.decode(instr.encode())
            decoded shouldBe instr
        }
    }
})
```

- [ ] **Step 4: 테스트 — `AssemblerTest.kt`**

```kotlin
package risc8.ch13
import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class AssemblerTest : DescribeSpec({
    describe("RISC-8 Assembler") {
        it("ADD R1, R2, R3 어셈블") {
            val asm = Assembler.assemble("ADD R1, R2, R3")
            asm.words[0] shouldBe Instruction.Add(1, 2, 3).encode()
        }
        it("라벨 forward reference") {
            val src = """
                BEQ R0, R0, loop
                ...
                loop: HALT
            """.trimIndent()
            val asm = Assembler.assemble(src)
            // 라벨이 올바른 offset으로 채워졌는지
            asm.symbols["loop"] shouldBe 1
        }
    }
})
```

- [ ] **Step 5: 테스트 — `CpuFibTest.kt`**

```kotlin
package risc8.ch13
import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class CpuFibTest : DescribeSpec({
    describe("RISC-8 Fibonacci") {
        it("처음 10개 Fibonacci 메모리에 저장") {
            val src = javaClass.getResource("/programs/fib.risc8")!!.readText()
            val asm = Assembler.assemble(src)
            val cpu = Cpu(asm.words)
            cpu.run(maxCycles = 10_000)
            val fib10 = (0..9).map { cpu.memory[0x100 + it] }
            fib10 shouldBe listOf(0,1,1,2,3,5,8,13,21,34)
        }
    }
})
```

- [ ] **Step 6: `programs/fib.risc8`**

```
; RISC-8 Fibonacci (10개를 메모리 0x100~0x109에 저장)
        LI    R1, 0           ; F(0)
        LI    R2, 1           ; F(1)
        LI    R3, 0x100       ; 결과 베이스 주소
        LI    R4, 10          ; counter
        LI    R5, 0           ; index
loop:   STB   R1, R3, R5      ; mem[R3 + R5] = R1
        ADD   R6, R1, R2      ; R6 = F(n+1)
        ADD   R1, R0, R2      ; R1 = F(n+1)
        ADD   R2, R0, R6      ; R2 = F(n+2)
        ADD   R5, R5, R1      ; index++... (실제로는 ADDI 필요)
        BNE   R5, R4, loop
        HALT
```

(실제 명령어 인코딩은 ISA에 맞게 책 13장의 코드를 따른다.)

- [ ] **Step 7: 구현 — `Isa.kt`, `Assembler.kt`, `Cpu.kt`, `Risc8Demo.kt`**

책 13_final.md의 코드 블록을 따른다. sealed class Instruction (R/I/J subtype), Assembler 2-pass, Cpu (16 registers + 256 bytes RAM + decode dispatch).

- [ ] **Step 8: build.gradle.kts**

```kotlin
plugins { alias(libs.plugins.kotlin.jvm); application }
application { mainClass.set("risc8.ch13.Risc8DemoKt") }
```

- [ ] **Step 9: 테스트 통과 + 데모 실행**

```bash
./gradlew :chapter-13:test
./gradlew :chapter-13:run
```
Expected: Fibonacci 0,1,1,2,3,5,8,13,21,34 출력.

- [ ] **Step 10: 커밋**

```bash
git add example/chapter-13/
git commit -m "Add chapter-13 RISC-8 ISA + Assembler + Cpu (Fibonacci runs)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 15: Chapter 14 — CycleAccurate + JMH 벤치마크

**책 참조:** `kotlin-8bit-cpu/chapters/14_final.md`

**Files:**
- Create: `example/chapter-14/build.gradle.kts`, `README.md`
- Copy from chapter-13 (rename to ch14): Isa, Assembler, Cpu
- Create: `example/chapter-14/src/main/kotlin/risc8/ch14/CycleAccurate.kt` — 명령별 cycle 비용 + cycle counter
- Create: `example/chapter-14/src/main/kotlin/risc8/ch14/CycleDemo.kt`
- Create: `example/chapter-14/src/jmh/kotlin/risc8/ch14/CpuBenchmark.kt`
- Create: `example/chapter-14/src/test/kotlin/risc8/ch14/CycleAccurateTest.kt`

- [ ] **Step 1: chapter-13 복사 + rename**

- [ ] **Step 2: `build.gradle.kts` (JMH 플러그인 추가)**

```kotlin
plugins {
    alias(libs.plugins.kotlin.jvm)
    application
    alias(libs.plugins.jmh)
}

application { mainClass.set("risc8.ch14.CycleDemoKt") }

jmh {
    fork.set(1)
    iterations.set(3)
    warmupIterations.set(2)
}
```

- [ ] **Step 3: 테스트 — `CycleAccurateTest.kt`**

```kotlin
package risc8.ch14
import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe

class CycleAccurateTest : DescribeSpec({
    describe("CycleAccurate Cpu") {
        it("ADD는 1 cycle") {
            val cpu = CycleAccurateCpu(intArrayOf(Instruction.Add(1, 2, 3).encode()))
            cpu.step()
            cpu.cycleCount shouldBe 1
        }
        it("LDB는 2 cycles (메모리 접근)") {
            val cpu = CycleAccurateCpu(intArrayOf(Instruction.Ldb(rd=1, rs1=0, imm=0x10).encode()))
            cpu.step()
            cpu.cycleCount shouldBe 2
        }
        it("BEQ taken은 2 cycles, not taken은 1 cycle") {
            // ...
        }
    }
})
```

- [ ] **Step 4: 구현 — `CycleAccurate.kt`**

```kotlin
package risc8.ch14

class CycleAccurateCpu(program: IntArray) {
    private val cpu = Cpu(program)
    var cycleCount: Long = 0L
        private set

    fun step() {
        val instr = decodeAt(cpu.pc)
        cycleCount += cyclesFor(instr)
        cpu.step()
    }
    fun run(maxCycles: Long = Long.MAX_VALUE) {
        while (!cpu.halted && cycleCount < maxCycles) step()
    }
    private fun cyclesFor(instr: Instruction): Int = when (instr) {
        is Instruction.Add, is Instruction.Sub, is Instruction.And, ... -> 1
        is Instruction.Ldb, is Instruction.Stb -> 2
        is Instruction.Beq, is Instruction.Bne -> if (taken(instr)) 2 else 1
        is Instruction.Jal -> 2
        ...
    }
}
```

- [ ] **Step 5: JMH 벤치 — `CpuBenchmark.kt`**

```kotlin
package risc8.ch14

import org.openjdk.jmh.annotations.*
import java.util.concurrent.TimeUnit

@State(Scope.Benchmark)
@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.SECONDS)
open class CpuBenchmark {
    private lateinit var fibProgram: IntArray

    @Setup
    fun setup() {
        val src = javaClass.getResource("/programs/fib.risc8")!!.readText()
        fibProgram = Assembler.assemble(src).words.toIntArray()
    }

    @Benchmark
    fun instructionAccurate(): Long {
        val cpu = Cpu(fibProgram)
        cpu.run(maxCycles = 10_000)
        return cpu.pc.toLong()
    }

    @Benchmark
    fun cycleAccurate(): Long {
        val cpu = CycleAccurateCpu(fibProgram)
        cpu.run(maxCycles = 10_000)
        return cpu.cycleCount
    }
}
```

- [ ] **Step 6: 테스트 통과 + 데모 + 벤치 실행 확인**

```bash
./gradlew :chapter-14:test
./gradlew :chapter-14:run
./gradlew :chapter-14:jmh   # JMH 실행 (시간 좀 걸림)
```

- [ ] **Step 7: 커밋**

```bash
git add example/chapter-14/
git commit -m "Add chapter-14 cycle-accurate RISC-8 + JMH benchmark

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 16: Chapter 15 — README only (다음 봉우리 청사진)

**Files:**
- Create: `example/chapter-15/README.md`

- [ ] **Step 1: README 작성**

책 15장의 핵심: CPU → 컴퓨터 전체 → 커널 → OS → Application으로 가는 다음 12개월 청사진. README는 그 청사진을 한 페이지로 요약 + 추천 자료 (nand2tetris, OSTEP, Crafting Interpreters, Operating Systems from 0 to 1).

- [ ] **Step 2: 커밋**

```bash
git add example/chapter-15/
git commit -m "Add chapter-15 next-mountain blueprint (README only)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 17: 최종 검증 — 전체 빌드·테스트·데모

**Files:** (없음 — 검증만)

- [ ] **Step 1: 전체 빌드**

```bash
cd example
./gradlew clean build
```
Expected: BUILD SUCCESSFUL, 0 failures.

- [ ] **Step 2: 전체 테스트**

```bash
./gradlew test
```
Expected: 모든 챕터 테스트 통과.

- [ ] **Step 3: 데모 실행 확인 (5개 챕터의 run 태스크)**

```bash
./gradlew :chapter-02:run
./gradlew :chapter-06:run
./gradlew :chapter-07:run
./gradlew :chapter-09:run
./gradlew :chapter-10:run
./gradlew :chapter-13:run
./gradlew :chapter-14:run
```
Expected:
- ch02 → `Accumulator = 42`
- ch06 → `OUT = 47`
- ch07 → `어셈블 → 실행 → OUT = 47`
- ch09 → `Hello, World!`
- ch10 → debugger CLI 진입 (q로 종료)
- ch13 → Fibonacci 출력
- ch14 → cycle count + Fibonacci

- [ ] **Step 4: 챕터별 코드 라인 수 보고 (참고)**

```bash
find example -name "*.kt" -path "*/main/*" | xargs wc -l | tail -1
find example -name "*.kt" -path "*/test/*" | xargs wc -l | tail -1
```

- [ ] **Step 5: README 매트릭스 최종 점검**

`example/README.md`의 챕터 매트릭스가 실제 구현과 일치하는지 확인. 필요 시 수정·재커밋.

- [ ] **Step 6: 마지막 커밋 (verification 메모)**

```bash
git commit --allow-empty -m "Verify example/ build + all chapter demos run

15-chapter Gradle multi-module project complete.
All tests pass, all demos run.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review 메모

**스펙 커버리지:**
- ✓ 누적 스냅샷 (각 챕터 Task에 "chapter-(N-1) 복사 + rename" 단계 명시)
- ✓ Gradle Kotlin DSL (Task 1에 settings·build·libs.versions·wrapper 모두)
- ✓ JVM 17 (Task 1 build.gradle.kts의 `jvmToolchain(17)`)
- ✓ kotest 5.x (Task 1 libs.versions.toml + 모든 챕터 테스트 DescribeSpec)
- ✓ application 플러그인 (Task 3, 7, 8, 10, 14, 15에 mainClass)
- ✓ 챕터 1·12·15 README only (Task 2, 13, 16)
- ✓ 챕터 11 asm 파일 (Task 12)
- ✓ JMH (Task 15에 me.champeau.jmh + benchmark 클래스)
- ✓ 데모 실행 가능 (Task 17 검증)

**Type 일관성:**
- chapter-06의 SAP-1 통합 테스트가 `Sap1` 클래스를 쓰고, chapter-07은 같은 패키지 (sap.ch07)에서 `Sap1`을 재사용 (rename된 복사본). ✓
- chapter-09의 `assembleAndRun` helper가 모든 demo와 test에서 일관 사용. ✓
- chapter-13/14의 RISC-8 명령어는 sealed class Instruction → encode/decode round-trip을 IsaTest에서 검증. ✓

**Placeholder 스캔:**
- "..." 사용처: 코드 본문이 일부 생략된 곳(`MicroRom`, `DebuggerCli`, `Cpu` 등). 이는 책 본문이 권위라는 정책상 의도적. 각 Task에 책 챕터 파일 경로를 명시했으므로 구현자가 그곳을 참조할 수 있음.
- 명확하지 않은 "TODO/TBD" 없음. ✓

**Scope:**
- 17개 Task, 챕터 단위로 분할. 한 Task = 한 챕터 = 자기 완결적 commit. ✓

---
