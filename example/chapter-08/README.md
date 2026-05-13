# 8장 — 16바이트의 한계: SAP-2는 왜 다시 설계되었는가

## 핵심 질문

- 5개 명령어와 16바이트로 무엇을 할 수 없는가?
- Fibonacci 수열을 SAP-1으로 짜보면 무엇이 막히는가?
- Malvino는 왜 SAP-2를 "근본 재설계"라 불렀는가?
- 레지스터가 하나뿐인 CPU는 어디까지 갈 수 있는가?
- 주소 버스 4비트를 16비트로 늘린다는 것은 무엇을 의미하는가?

---

## SAP-1의 한계를 직접 부딪혀 보자

SAP-1을 구현했을 때 우리는 무언가를 '만들었다'는 느낌을 받았을 것이다. 실제로 더하고 빼고 멈추는 CPU가 Kotlin 코드로 돌아갔다. 그런데 Fibonacci 수열을 SAP-1으로 짜려고 시도하면 어떤 일이 벌어질까?

```
; SAP-1로 Fibonacci를 시도하면…
LDA 0x0   ; a = memory[0]
ADD 0x1   ; a = a + memory[1]  -- 결과를 어디 저장하지?
           ; memory에 쓰는 명령어가 없다!
           ; 레지스터가 1개뿐이라 a, b 두 값을 동시에 못 잡는다
           ; 반복(loop)을 위한 점프 명령어가 없다
           ; 프로그램이 16바이트를 넘으면 시작도 못 한다
HLT
```

이것이 SAP-1의 현실이다. 루프도, 저장도, 공간도 없다.

---

## SAP-2: 무엇이 바뀌었는가

| 항목 | SAP-1 | SAP-2 |
|------|-------|-------|
| 메모리 | 16바이트 (4비트 주소) | 64KB (16비트 주소) |
| 명령어 수 | 5개 | 39개 |
| 레지스터 | 누산기(A) 1개 | 범용 레지스터 A, B, C |
| 점프 | 없음 | JMP, JZ, JNZ 등 조건 분기 |
| 서브루틴 | 없음 | CALL / RET |
| 입출력 | 없음 | IN / OUT |

주소 버스가 4비트에서 16비트로 늘어나는 것은 단순한 숫자 변화가 아니다. 프로그램이 '공간'을 얻는 것이다. 데이터를 쌓아둘 스택이 생기고, 서브루틴을 호출할 수 있고, 실제로 쓸 만한 프로그램을 담을 수 있게 된다.

레지스터가 A, B, C 세 개로 늘어나는 것도 마찬가지다. 두 값을 동시에 손에 쥐고 연산할 수 있어야 비로소 Fibonacci 같은 계산이 가능해진다.

---

## 이 챕터의 범위: scaffold

이 챕터에서는 SAP-2의 뼈대(scaffold)를 세운다.

- **`Sap2Core`** — 64KB `IntArray` 메모리, 16비트 PC, fetch/read/write/halt/reset
- **`RegisterFile`** — 8비트 레지스터 A, B, C를 하나로 묶은 파일

ALU 연산, 분기 명령어, CALL/RET, I/O, 인터럽트는 9장에서 본격적으로 구현한다.

### SAP-2 ISA는 "Intel 8080 subset"

SAP-2의 명령어 집합은 Malvino가 Intel 8080을 가르치기 위해 의도적으로 간추린 부분집합이다. 레지스터 이름(A, B, C), 명령어 형식, 플래그 동작이 모두 8080의 것이다. 9장에서 SAP-2 실행기를 완성하고 나면, 우리는 사실상 8080 에뮬레이터의 핵심을 손으로 만든 것이 된다.

---

## 테스트

```
./gradlew :chapter-08:test
```

| 테스트 클래스 | 검증 항목 |
|---------------|-----------|
| `Sap2CoreTest` | 64KB 메모리 크기, 16비트 PC 마스킹, 0xFFFF→0 wrap, fetch, writeByte/readByte 8비트 마스킹, halt, reset |
| `RegisterFileTest` | A/B/C 초기 0, 개별 load, reset 후 전체 0 |
| (ch07 이관) | AluFlags, ProgramCounter, Register, Clock, Instruction, Assembler, Lexer, SAP-1 통합 |

---

## 산출물

```
chapter-08/
└── src/
    ├── main/kotlin/sap/ch08/
    │   ├── Sap2Core.kt       ← 신규: 64KB RAM + 16비트 PC
    │   ├── RegisterFile.kt   ← 신규: A/B/C 레지스터 파일
    │   ├── Register.kt
    │   ├── AluFlags.kt
    │   ├── Bus.kt
    │   ├── Clock.kt
    │   ├── Controller.kt
    │   ├── Instruction.kt
    │   ├── ProgramCounter.kt
    │   ├── Ram.kt
    │   ├── Sap1.kt
    │   └── asm/
    │       ├── Assembler.kt
    │       ├── Lexer.kt
    │       └── Token.kt
    └── test/kotlin/sap/ch08/
        ├── Sap2CoreTest.kt
        ├── RegisterFileTest.kt
        └── (ch07 이관 테스트들)
```
