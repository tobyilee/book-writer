# 9장 — 조건 분기·서브루틴·I/O: CPU가 "결정"하는 순간

## 핵심 질문

- 분기 명령어가 없는 CPU는 왜 그렇게 답답한가? if·while·function 호출은 기계어 수준에서 무엇으로 환원되는가?
- 스택은 왜 "주소를 저장하기 위한 자료구조"가 아니라 "CPU가 호출을 떠나기 위한 길"인가?
- 입출력은 메모리와 어떻게 다른가? 그리고 왜 8080은 별도 포트 공간을, 6502는 메모리 매핑을 택했는가?

이 챕터에서 SAP-2 실행기를 완성하면, 우리는 처음으로 "프로그램이 분기하고 함수가 호출되고 외부 세계에 글자가 흘러나가는" CPU를 손에 쥐게 된다. 8장에서 세운 64KB·세 레지스터·16비트 PC의 뼈대 위에, 마침내 살이 붙는다.

---

## SAP-2 ISA: 본 책의 부분집합

8080의 명령어 집합 전체를 흉내내려는 게 아니다. Hello와 Fibonacci 두 데모를 정확히 돌릴 수 있는 가장 작은 ISA를 고른다. 명령어 1바이트(operand 길이는 가변)로 인코딩한다.

| 니모닉 | 인코딩 | 동작 |
|---|---|---|
| `NOP` | `0x00` | 아무것도 하지 않는다 |
| `LDI A, imm8` | `0x01 imm8` | `A = imm8` |
| `LDI B, imm8` | `0x02 imm8` | `B = imm8` |
| `LDI C, imm8` | `0x03 imm8` | `C = imm8` |
| `MOV A, B` | `0x10` | `A = B` |
| `MOV A, C` | `0x11` | `A = C` |
| `MOV B, A` | `0x12` | `B = A` |
| `MOV C, A` | `0x13` | `C = A` |
| `MOV B, C` | `0x14` | `B = C` |
| `MOV C, B` | `0x15` | `C = B` |
| `ADD B` | `0x20` | `A = A + B`, Z 갱신 |
| `ADD C` | `0x21` | `A = A + C`, Z 갱신 |
| `SUB B` | `0x22` | `A = A - B`, Z 갱신 |
| `INC A/B/C` | `0x30..0x32` | `r = r + 1`, Z 갱신 |
| `DEC A/C` | `0x33, 0x34` | `r = r - 1`, Z 갱신 |
| `JMP addr16` | `0x40 lo hi` | `PC = addr` |
| `JZ addr16` | `0x41 lo hi` | `Z`이면 `PC = addr` |
| `JNZ addr16` | `0x42 lo hi` | `Z`가 아니면 `PC = addr` |
| `CALL addr16` | `0x50 lo hi` | 반환 주소를 스택에 push, `PC = addr` |
| `RET` | `0x51` | 스택에서 pop한 값을 `PC`에 적재 |
| `IN port` | `0x60 port` | `A = inputPorts[port]` |
| `OUT port` | `0x61 port` | `outputPorts[port] = A` |
| `HLT` | `0xFF` | 정지 |

플래그는 일단 Zero(Z) 하나만 둔다. ADD/SUB/INC/DEC의 결과가 0이면 세팅된다. Sign·Carry 플래그는 본 책의 단순화 SAP-2에서 다루지 않는다(8080 풀 셋은 11장에서 부분적으로 확장한다).

---

## 분기 — `if`가 기계어로 내려갔을 때

고수준 언어의 `if (x == 0) ...`는 컴파일러를 거쳐 두 줄로 환원된다.

```
        DEC A       ; 비교(여기서는 0과의 비교를 위해 단순히 감소시킨다)
        JZ  label
```

분기 명령이 하는 일은 단순하다 — PC를 다른 주소로 옮긴다. 그게 전부다. 그런데 그 단순한 동작 하나가 "프로그램이 흐름을 결정한다"는 추상 개념의 물리적 근거가 된다. 분기 없는 CPU는 결정하지 못한다. 그저 흘러갈 뿐이다.

테스트 `Sap2InstructionsTest.kt`에서 `JZ`·`JNZ`·`JMP`가 어떻게 PC를 갈아끼우는지 한 줄씩 확인한다.

---

## 서브루틴 — 스택은 "돌아갈 길"이다

`CALL addr`는 두 가지 일을 동시에 한다.

1. 지금 PC(반환 주소)를 스택에 push한다.
2. PC를 addr로 옮긴다.

`RET`은 그 역순이다 — 스택에서 pop한 값을 PC에 적재한다. 스택을 자료구조로만 보면 "왜 이런 게 CPU에 들어 있지?"가 자연스러운 질문이다. 그런데 함수 호출 측면에서 보면, 스택은 **CPU가 자기가 어디서 왔는지를 기억하는 유일한 방법**이다. 호출이 중첩될 수 있는 한, 반환 주소도 중첩되어야 한다. 스택이 LIFO인 이유가 거기 있다.

본 책의 SAP-2는 SP를 0xFFFE에서 시작하고 push 때마다 2바이트씩 감소시킨다(8080 관례). 메모리의 윗쪽을 스택이 거꾸로 자라며 차지하고, 프로그램은 아랫쪽에서 시작해 위로 자란다 — 둘이 충돌하면 스택 오버플로다.

```kotlin
0x50 -> {                              // CALL
    val addr = fetch16()
    val retAddr = core.pc              // 다음 명령어 주소
    core.writeByte(sp,         retAddr and 0xFF)
    core.writeByte(sp - 1, (retAddr shr 8) and 0xFF)
    sp = (sp - 2) and 0xFFFF
    core.setPc(addr)
}
```

---

## I/O — 메모리 매핑 vs 별도 포트

8080은 별도 I/O 명령(`IN`/`OUT`)과 8비트 포트 주소 공간을 두었다. 6502는 그런 명령이 없는 대신 특정 메모리 주소를 I/O 장치에 매핑했다(memory-mapped I/O). 둘 다 장단이 있다.

| 방식 | 장점 | 단점 |
|---|---|---|
| 별도 포트 (8080) | 명령어가 명시적, 메모리 공간 절약 | I/O 명령을 따로 학습해야 함 |
| 메모리 매핑 (6502, ARM, RISC-V) | 명령어가 적고, 같은 LOAD/STORE로 처리 | I/O가 메모리 공간을 차지 |

본 책의 SAP-2는 8080 쪽을 택한다 — `IN port` / `OUT port` 명령이 따로 있고, 16개의 입력 포트와 16개의 출력 포트가 있다. 출력 포트 0은 ASCII 스트림으로 약속한다(테스트 가능성 때문).

인터럽트는 이 챕터의 범위가 아니다 — 폴링 기반 I/O만 다룬다. 인터럽트 컨트롤러는 12장에서 직접 만든다.

---

## 두 데모

### `Hello` — 가장 작은 출력

```
LDI A, 'H'
OUT 0
LDI A, 'e'
OUT 0
...
LDI A, 10      ; '\n'
OUT 0
HLT
```

문자 6개를 한 번에 하나씩 누산기에 넣고 포트 0으로 흘려보낸다. 어셈블러는 `'H'` 같은 문자 리터럴을 ASCII 코드(0x48)로 변환한다. 결과는 호스트 콘솔에 `Hello\n` 한 줄.

### `Fibonacci` — 분기는 아니지만 누산기 1개로 두 값을 굴리는 패턴

본 책의 SAP-2 ISA에는 메모리 LOAD/STORE가 없고(11장에서 추가) ADD도 `A = A + (B or C)` 형태뿐이다. 그래서 카운터를 두고 루프로 돌리는 대신, F0~F9까지 8번 펼친 직선 코드를 쓴다. 핵심은 매 사이클마다 B(prev), C(curr), A(next)의 역할을 회전시키는 것이다.

```
        MOV A, B       ; A = prev
        ADD C          ; A = prev + curr = next
        OUT 0          ; emit next
        MOV B, C       ; prev <- curr
        MOV C, A       ; curr <- next
```

다섯 줄짜리 블록을 여덟 번 펼치면 0, 1, 1, 2, 3, 5, 8, 13, 21, 34가 차례로 나온다. 분기·CALL·RET은 `Sap2InstructionsTest`에서 단독으로 검증한다.

> **루프로 더 짧게 못 쓰나?** 쓸 수 있다. 카운터를 메모리에 두고 `DEC C`, `JNZ loop` 패턴을 만들면 된다. 다만 본 책의 SAP-2는 `LDA addr` 같은 메모리 적재가 없어서 카운터를 레지스터에만 둬야 하는데, 그러면 fib 계산용 B/C와 충돌한다. 11장에서 메모리 명령어가 추가되면 루프 버전도 가능해진다.

---

## 실행

```
./gradlew :chapter-09:run        # Hello 데모
./gradlew :chapter-09:runFib     # Fibonacci 데모
./gradlew :chapter-09:test       # 전체 테스트
```

기대 출력:

```
$ ./gradlew :chapter-09:run --quiet
Hello

$ ./gradlew :chapter-09:runFib --quiet
Fibonacci (first 10): 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
```

---

## 테스트

| 테스트 클래스 | 검증 항목 |
|---|---|
| `Sap2HelloTest` | hello.sap2 어셈블 + 실행 → port 0 출력이 "Hello\n" |
| `Sap2FibTest` | fib.sap2 어셈블 + 실행 → port 0 출력이 [0,1,1,2,3,5,8,13,21,34] |
| `Sap2InstructionsTest` | LDI/MOV/ADD/SUB/DEC/INC/JMP/JZ/JNZ/CALL+RET/IN/OUT, zero flag, INC wrap, SP 원복, 문자 리터럴 |
| (ch08 이관) | Sap2Core, RegisterFile, AluFlags, ProgramCounter, Register, Clock, Instruction, Assembler, Lexer, SAP-1 통합 |

총 80 테스트 통과.

---

## 산출물

```
chapter-09/
├── build.gradle.kts          ← application 플러그인 + runFib task
├── src/
│   ├── main/
│   │   ├── kotlin/sap/ch09/
│   │   │   ├── Sap2.kt              ← 신규: SAP-2 실행기(분기·스택·I/O)
│   │   │   ├── Sap2Util.kt          ← 신규: assembleAndRun 헬퍼
│   │   │   ├── HelloDemo.kt         ← 신규: Hello 데모 main
│   │   │   ├── FibDemo.kt           ← 신규: Fibonacci 데모 main
│   │   │   ├── Sap2Core.kt          ← ch08 이관
│   │   │   ├── RegisterFile.kt      ← ch08 이관
│   │   │   ├── (Sap1·Register·AluFlags·Bus·Clock·Controller·Instruction·ProgramCounter·Ram)
│   │   │   └── asm/
│   │   │       ├── Sap2Assembler.kt ← 신규: 2-pass SAP-2 어셈블러(레이블·문자 리터럴)
│   │   │       └── (Assembler·Disassembler·Lexer — ch08 이관)
│   │   └── resources/programs/
│   │       ├── hello.sap2           ← 신규
│   │       ├── fib.sap2             ← 신규
│   │       └── add.sap1             ← ch08 이관
│   └── test/kotlin/sap/ch09/
│       ├── Sap2HelloTest.kt         ← 신규
│       ├── Sap2FibTest.kt           ← 신규
│       ├── Sap2InstructionsTest.kt  ← 신규
│       └── (Sap2CoreTest, RegisterFileTest, … — ch08 이관)
```
