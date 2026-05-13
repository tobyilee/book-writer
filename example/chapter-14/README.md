# 14장 — instruction-accurate에서 cycle-accurate로

> **핵심 한 줄:** 13장 RISC-8 시뮬레이터는 "명령어 하나 = 한 박자"였다. 14장에서는 명령어마다 진짜 사이클 비용을 매겨, 메모리 접근·분기 미스 같은 stall을 모델링한다. 결과는 같지만, 사이클 수가 다르다 — 같은 프로그램에서 평균 CPI(Cycles Per Instruction)가 보인다.

---

## 이 장이 던지는 질문

instruction-accurate 시뮬레이터는 빠르고 쉽다. 프로그램이 의미적으로 무얼 하는지 확인하는 데에는 그게 전부면 충분하다. 그런데 책 앞쪽에서 인터럽트 latency를 이야기할 때 슬쩍 비집고 들어온 의문이 있었다 — "이 명령어는 사이클 몇 개야?"

이 한 줄을 진지하게 받으면 시뮬레이터 모델이 달라진다. 메모리에서 한 바이트 읽는 LB는 ALU에서 두 수를 더하는 ADD보다 비싸야 한다. 잡힌 분기는 그렇지 않은 분기보다 비싸야 한다 — 진짜 파이프라인이라면 fetch한 다음 명령어를 버려야 하니까.

그래서 본 챕터에서는 **cycle-accurate 시뮬레이터**를 만든다. 13장 코드를 옆에 두고, 그 위에 "명령어별 사이클 비용 테이블"을 얹는 식으로.

---

## 두 모델, 한 ISA

| 구분 | instruction-accurate (13장) | cycle-accurate (14장) |
|------|----------------------------|----------------------|
| 단위 | 명령어 1개 = 1 step | 명령어 1개 = 1~2 cycle |
| 의미적 결과 | 정확 | 정확 (동일) |
| 분기 미스 모델 | 없음 | taken 분기 +1 cycle |
| 메모리 stall 모델 | 없음 | LB/SB +1 cycle |
| 용도 | 정확성 검증, 디버깅 | 성능 분석, latency 검증 |
| 속도 | 가장 빠름 | 약간 느림 (디코드 1회 추가) |

같은 프로그램의 의미적 결과는 정확히 일치한다 — register와 memory 상태가 동일하다. 다른 건 "그게 몇 사이클 들었느냐"뿐이다.

---

## RISC-8 사이클 비용 표

본 챕터의 cycle-accurate 모델은 **단일 이슈 in-order 5-stage 파이프라인**의 최소 근사다. 진짜 칩의 비용 모델과는 다르지만, 모델이 무엇을 보여주려 하는지는 똑같다.

| 명령어 그룹 | cycle | 사유 |
|-------------|-------|------|
| `ADD/SUB/AND/OR/XOR/SHL/SHR` (R-type) | 1 | ALU 한 박자 |
| `ADDI/ANDI/LI` (I·L-type 산술) | 1 | 즉치는 디코드에서 바로 |
| `LB/SB` | **2** | 메모리 접근 1 cycle stall |
| `BEQ/BNE` — taken | **2** | 분기 잡히면 파이프라인 flush |
| `BEQ/BNE` — not taken | 1 | 분기 예측 적중과 동치 |
| `JAL/JR` | **2** | 무조건 점프도 fetch slot 1개 버림 |
| `NOP/ECALL/EBREAK/HALT` | 1 | 부수효과만 |

이 표가 본 챕터의 핵심 데이터다. 사이클 모델을 늘리거나 줄이는 일은 표의 숫자를 바꾸는 일이다.

---

## 같은 Fibonacci, 두 시뮬레이터

13장의 `fib.risc8`을 그대로 옮겨와 두 모델로 돌려본다.

```bash
./gradlew :chapter-14:run
```

기대 출력:

```
--- 같은 Fibonacci, 두 시뮬레이터 ---
프로그램 워드 수: 14
instruction-accurate 사이클 (= 실행한 명령어 수): 85
cycle-accurate 총 사이클: 105
평균 CPI(Cycles Per Instruction): 1.24

memory[0x10..0x19] (cycle-accurate):
0, 1, 1, 2, 3, 5, 8, 13, 21, 34

memory[0x10..0x19] (instruction-accurate):
0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

명령어 85개 → 사이클 105개. CPI가 1.24다. 그 0.24의 출처는 명령어 종류별로 추적할 수 있다 — SB·LB가 10개씩, JAL이 9번, 잡힌 BEQ가 1번. 더한 cycle 페널티가 정확히 20이다.

> **CPI는 어디서 와서 어디로 가는가**
>
> CPI < 1.0은 superscalar(한 사이클에 명령어 여러 개)로 가야 나온다. RISC-8 모델은 단일 이슈라 CPI ≥ 1.0이 늘 성립한다. 진짜 CPU에서 CPI를 줄이는 길은 두 갈래 — 명령어를 한 박자에 여러 개 끝내거나(superscalar/OoO), 사이클당 일을 늘리는 것(SIMD). RISC-V Rocket·BOOM에서 후속이 이어진다.

---

## 인터럽트 latency 회수

책 앞쪽에서 인터럽트 latency를 짚었다 — "인터럽트가 들어와도 현재 명령어가 끝나야 다음 fetch에서 핸들러로 점프한다, 그래서 worst-case latency는 가장 긴 명령어의 사이클 수에 좌우된다." instruction-accurate 모델로는 그걸 측정할 수 없다. 모든 명령어가 1 step이니까.

cycle-accurate 모델은 그 이야기를 측정 가능한 수치로 바꾼다. RISC-8 worst-case 명령어는 LB·SB·JAL·taken-BEQ 중 어떤 것이든 2 cycle이다 — 그러니 인터럽트 latency 상한은 2 cycle + 핸들러 진입 cost다. 진짜 시스템에서 cycle-accurate 시뮬레이터가 RTOS 검증에 쓰이는 이유가 여기 있다.

---

## JMH 벤치마크

cycle-accurate가 instruction-accurate보다 얼마나 느릴까? 한 번 더 명령어 디코딩이 일어나고 사이클 비용 계산이 추가됐으니 조금 느려야 한다. 그런데 얼마나? 감으로 짐작하지 말고 측정해보자.

```bash
./gradlew :chapter-14:jmh
```

JMH(Java Microbenchmark Harness)는 JVM 워밍업·dead code elimination·timing 보정을 자동으로 처리하는 표준 마이크로벤치 도구다. 본 챕터에서는 fork 1·warmup 2·measurement 3 × 1초 — 약 15초쯤이면 끝난다.

```
Benchmark                              Mode  Cnt    Score    Error   Units
CpuBenchmark.cycleAccurate            thrpt    3  XXXX.XX ± YYY.YY  ops/ms
CpuBenchmark.instructionAccurate      thrpt    3  XXXX.XX ± YYY.YY  ops/ms
```

(실제 숫자는 머신마다 다르지만, instruction-accurate가 1.1~1.5배쯤 빠른 게 보통이다.)

> **왜 JMH인가**
>
> 마이크로벤치는 `System.nanoTime()`으로 직접 재면 JIT 컴파일 타이밍·escape analysis·반환값 사장에 영향을 받아 의미 없는 숫자가 나온다. JMH의 `@Benchmark`·`Blackhole`·forked JVM 모델은 그 함정을 막아준다. JMH가 "측정 가능한 코드"를 강제로 만드는 셈이다.

---

## 테스트

```bash
./gradlew :chapter-14:test
```

- `IsaTest` — 13장과 동일 (encode/decode 라운드트립)
- `AssemblerTest` — 13장과 동일 (라벨 해석, 즉치 처리)
- `CpuFibTest` — 13장과 동일 (instruction-accurate 의미 검증)
- `CycleAccurateTest` — **본 챕터 신규** — 명령어별 cycle 비용, taken/not-taken 분기, 의미적 동치성

cycle-accurate 모델이 13장 모델과 register·memory 결과를 한 자리 어긋남 없이 일치시키는 것이 마지막 테스트의 핵심이다 — "성능 모델을 바꿔도 정확성은 안 깨진다"는 보증.

---

## 산출물

```
src/main/kotlin/risc8/ch14/
├── Isa.kt            — 13장과 동일
├── Assembler.kt      — 13장과 동일
├── Cpu.kt            — 13장과 동일 (instruction-accurate)
├── CycleAccurate.kt  — 본 챕터 신규 (cycle-accurate wrapper)
└── CycleDemo.kt      — 두 모델 비교 데모

src/jmh/kotlin/risc8/ch14/
└── CpuBenchmark.kt   — JMH 벤치마크 (instruction vs cycle accurate)

src/main/resources/programs/
└── fib.risc8         — 13장과 동일

src/test/kotlin/risc8/ch14/
├── IsaTest.kt
├── AssemblerTest.kt
├── CpuFibTest.kt
└── CycleAccurateTest.kt
```

---

## 관련 챕터

- **13장** — RISC-8 ISA·instruction-accurate 시뮬레이터 — 본 챕터의 출발점
- **15장** — 여기서 어디로 — cycle-accurate가 RISC-V 검증 환경(Spike, Verilator)으로 이어지는 다리
