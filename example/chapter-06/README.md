# 6장 — 메모리·버스·컨트롤러 — SAP-1이 처음 돌아가는 순간

> "각 모듈은 다 돌아가는데, 합치니 안 돌아가더라."
> 자작 CPU 입문자가 가장 많이 흘리는 한 줄이다.

## 핵심 질문

분리된 모듈들은 어떻게 **하나의 CPU**가 되는가?
ALU·Register·PC·메모리가 각자 동작해도, 그것이 곧 컴퓨터는 아니다.
모듈을 잇는 **버스**와, 누가 언제 버스에 올라타는지 명령하는 **컨트롤러**가 있어야
비로소 한 줄의 프로그램이 흐른다.

## 이 장에서 만드는 것

5장까지 우리 손에는 부품이 있었다.

- `AluFlags` — 8비트 산술과 4개 플래그
- `Register` — A·B·OUT
- `ProgramCounter` — 0..15 카운터
- `Instruction` — opcode 5종 디코더
- `Clock` — 단조 증가 카운터

이번 장에서 새로 만들 것은 세 가지다.

| 파일 | 역할 |
|------|------|
| `Ram.kt` | 16바이트 메모리 (주소 4비트, 데이터 8비트) |
| `Bus.kt` | W-bus 모델 — 한 번에 한 모듈만 올린다 |
| `Controller.kt` | (opcode, T-state) → control signal 집합 |
| `Sap1.kt` | 위 모두를 묶은 통합 시뮬레이터 |
| `Sap1Demo.kt` | 첫 프로그램을 실행하는 main |

## SAP-1 ISA — 한눈에

| Opcode | 명령 | 동작 |
|--------|------|------|
| `0x0X` | LDA X | `A = mem[X]` |
| `0x1X` | ADD X | `A = A + mem[X]` |
| `0x2X` | SUB X | `A = A - mem[X]` |
| `0xE0` | OUT | `output = A` |
| `0xF0` | HLT | 정지 |

상위 4비트가 opcode, 하위 4비트가 주소다.
16바이트 메모리이므로 주소도 4비트면 충분하다.

## 첫 프로그램 — 42 + 5

ROM 5바이트, 데이터 2바이트로 끝이다.

```
주소  바이트  뜻
0     0x09    LDA 9       ; A ← mem[9]
1     0x1A    ADD A       ; A ← A + mem[10]
2     0xE0    OUT         ; output ← A
3     0xF0    HLT
9     0x2A    42
A     0x05    5
```

실행하면 `output = 0x2F` (= 47). 첫 SAP-1 프로그램이 돌았다는 뜻이다.

## 구현 결정 — instruction-accurate vs cycle-accurate

원전(Malvino 『Digital Computer Electronics』)의 SAP-1은
명령 사이클을 **6 T-state**로 쪼갠다 — fetch 3 + execute 3.
각 T마다 어떤 control signal이 켜지는지 진리표가 있고,
W-bus 위에서 tri-state로 신호가 충돌 없이 흐른다.

하지만 우리는 지금 **첫 동작하는 SAP-1**이 목표다.
한 step()에서 fetch·decode·execute를 모두 끝내는 **instruction-accurate** 모델로 시작하자.
T-state 시각화·cycle-accurate 트레이스는 14장에서 본격적으로 다룬다.

`Controller`는 그래도 **신호 진리표의 윤곽**은 미리 박아둔다 —
14장에서 cycle-accurate로 갈 때 같은 인터페이스를 다시 쓰면 되도록.

```kotlin
Controller.signalsFor(opcode = 0x09, tState = 4)
// → { MEM_READ, LOAD_A }   ← LDA의 execute 단계
```

## 통합의 모양

`Sap1`은 모듈들의 owner다. 외부에는 `run()` / `step()` / `output` / `halted`만 노출한다.

```kotlin
class Sap1(rom: IntArray) {
    val ram = Ram(rom)
    val a = Register()
    val b = Register()
    val outReg = Register()
    val pc = ProgramCounter()

    fun run() { while (!halted) step() }
    fun step() { /* fetch → decode → execute */ }
}
```

`Sap1.run()`을 부른 뒤 `sap1.output`을 읽으면 그것이 우리의 첫 결과다.

## 실행

```bash
./gradlew :chapter-06:run
```

기대 출력:

```
OUT = 47 (0x2F)
Cycles: 4
```

테스트:

```bash
./gradlew :chapter-06:test
```

## GitHub 산출물

```
chapter-06/
├── build.gradle.kts
├── README.md
└── src/
    ├── main/kotlin/sap/ch06/
    │   ├── AluFlags.kt          (5장에서 그대로)
    │   ├── Bus.kt               ← 신규
    │   ├── Clock.kt
    │   ├── Controller.kt        ← 신규
    │   ├── Instruction.kt
    │   ├── ProgramCounter.kt
    │   ├── Ram.kt               ← 신규
    │   ├── Register.kt
    │   ├── Sap1.kt              ← 신규
    │   └── Sap1Demo.kt          ← 신규
    └── test/kotlin/sap/ch06/
        ├── AluFlagsOverflowSpec.kt
        ├── AluFlagsTest.kt
        ├── ClockTest.kt
        ├── InstructionTest.kt
        ├── ProgramCounterTest.kt
        ├── RegisterTest.kt
        └── Sap1IntegrationTest.kt   ← 신규
```

## 다음 장으로

손으로 ROM을 채우는 일은 오래 못 간다.
`0x1A`가 "ADD 10"인지 외우는 것은 두 명령이면 한계다.

다음 장은 **어셈블러**다.
`LDA 9 / ADD 10 / OUT / HLT`라는 텍스트를 받아
`0x09 0x1A 0xE0 0xF0`을 뱉는 작은 컴파일러를 만든다.
그 순간 우리는 **자기 언어를 가진 컴퓨터**의 첫 모서리를 만지게 된다.

---

> 참고: Albert Paul Malvino & Jerald A. Brown, *Digital Computer Electronics* 3rd ed., 1992 — SAP-1 원전.
